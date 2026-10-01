"""Exercise migration and update checks without touching the real Codex profile."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/sufficit/software-development/scripts/manage.py'
spec = importlib.util.spec_from_file_location('manage', SCRIPT)
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.source = self.root / manage.PACKAGE
        self.source.mkdir(parents=True)
        self.home = Path(self.temp.name) / 'codex'
        self.target, self.receipt = manage.paths(self.home)
        self.release = dict(name=manage.NAME, version='1.0.0', repository=manage.REPOSITORY, path=manage.PACKAGE)
        (self.source / 'release.json').write_text(json.dumps(self.release))
        (self.source / 'SKILL.md').write_text('---\nmetadata:\n  version: "1.0.0"\n---\nOriginal\n')
        (self.root / 'catalog').mkdir()
        (self.root / 'catalog/import-manifest.json').write_text(json.dumps({'skills': [dict(id=manage.NAME, path=manage.PACKAGE, contentSha256=manage.digest(self.source))]}))
        manage.git(self.root, 'init', '-b', 'main')
        manage.git(self.root, 'config', 'user.name', 'Test')
        manage.git(self.root, 'config', 'user.email', 'test@example.invalid')
        manage.git(self.root, 'remote', 'add', 'origin', manage.REPOSITORY + '.git')
        manage.git(self.root, 'add', '.')
        manage.git(self.root, 'commit', '-m', 'fixture')

    def original_copy(self):
        self.target.mkdir(parents=True)
        (self.target / 'SKILL.md').write_bytes(b'original user skill\n')

    def test_fresh_install_and_check(self):
        result = manage.install(self.source, self.home)
        self.assertEqual(self.target.resolve(), self.source)
        self.assertEqual(result['version'], '1.0.0')
        self.assertEqual(manage.check(self.source, self.home)['installation'], 'linked')
        self.assertEqual(manage.git(self.root, 'status', '--porcelain'), '')

    def test_migration_backup_and_idempotence(self):
        self.original_copy()
        first = manage.install(self.source, self.home, True)
        backup = Path(first['backup'])
        self.assertEqual((backup / 'SKILL.md').read_bytes(), b'original user skill\n')
        self.assertFalse(backup.is_relative_to(self.home / 'skills'))
        second = manage.install(self.source, self.home, True)
        self.assertEqual(second['backup'], first['backup'])
        self.assertEqual(len(list((self.home / 'skill-backups').iterdir())), 1)
        self.assertEqual(json.loads(self.receipt.read_text())['contentSha256'], manage.digest(self.source))

    def test_existing_copy_requires_explicit_migration(self):
        self.original_copy()
        with self.assertRaisesRegex(ValueError, 'preserved'):
            manage.install(self.source, self.home)
        self.assertFalse(self.target.is_symlink())
        self.assertEqual((self.target / 'SKILL.md').read_bytes(), b'original user skill\n')

    def test_foreign_link_is_preserved(self):
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(self.root / 'elsewhere')
        with self.assertRaisesRegex(ValueError, 'different source'):
            manage.install(self.source, self.home, True)
        self.assertEqual(self.target.readlink(), self.root / 'elsewhere')

    def test_modified_source_rejected(self):
        (self.source / 'SKILL.md').write_text('modified')
        with self.assertRaises(ValueError):
            manage.install(self.source, self.home)
        self.assertFalse(self.target.exists())

    def test_receipt_failure_restores_copy(self):
        self.original_copy()
        with patch.object(manage, 'write_receipt', side_effect=OSError('disk full')):
            with self.assertRaisesRegex(OSError, 'disk full'):
                manage.install(self.source, self.home, True)
        self.assertFalse(self.target.is_symlink())
        self.assertEqual((self.target / 'SKILL.md').read_bytes(), b'original user skill\n')
        self.assertEqual(list(self.target.parent.glob('.*stage*')), [])

    def test_remote_comparison_and_readonly_check(self):
        manage.install(self.source, self.home)
        local = manage.source_metadata(self.source)
        for version, digest, expected in [('1.0.0', local['contentSha256'], 'current'), ('1.0.0', '0'*64, 'version-conflict'), ('1.1.0', '0'*64, 'update-available'), ('0.9.0', '0'*64, 'local-ahead')]:
            with self.subTest(expected=expected), patch.object(manage, 'remote_metadata', return_value={**local, 'revision': 'f'*40, 'version': version, 'contentSha256': digest}):
                self.assertEqual(manage.check(self.source, self.home, True)['remote']['state'], expected)
        self.assertEqual(manage.git(self.root, 'status', '--porcelain'), '')
        self.assertEqual(manage.compare({'version': '1.9.0'}, {'version': '1.10.0'}), 'update-available')

    def test_network_failure_is_unknown(self):
        manage.install(self.source, self.home)
        with patch.object(manage, 'remote_metadata', side_effect=TimeoutError('offline')):
            result = manage.check(self.source, self.home, True)
        self.assertEqual(result['remote']['state'], 'unavailable')
        self.assertEqual(result['installation'], 'linked')

    def test_cli_checks_installed_fixture(self):
        manage.install(self.source, self.home)
        result = subprocess.run(['python3', '-B', str(SCRIPT), 'check', '--source', str(self.source), '--codex-home', str(self.home)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['installation'], 'linked')


if __name__ == '__main__':
    unittest.main()
