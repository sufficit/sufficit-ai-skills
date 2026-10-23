"""Repository documentation hierarchy and the behavior of its checker."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f'scripts/{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


coverage = load('markdown_coverage')
index = load('build_skill_index')
Graph = coverage.MarkdownGraph


class RepositoryTests(unittest.TestCase):
    def test_every_markdown_file_is_in_the_hierarchy(self):
        self.assertEqual(coverage.check(ROOT), [])

    def test_skill_index_is_current(self):
        self.assertEqual((ROOT / 'catalog/SKILLS.md').read_text(encoding='utf-8'), index.render(ROOT),
                         'run: python3 scripts/build_skill_index.py')


class GraphTests(unittest.TestCase):
    def test_reports_orphans_and_disconnected_cycles(self):
        graph = Graph({'README.md': '[Guide](guide.md)', 'guide.md': '[Root](README.md)',
                       'orphan.md': '[Self](orphan.md)', 'cycle-a.md': '[B](cycle-b.md)', 'cycle-b.md': '[A](cycle-a.md)'})
        self.assertEqual(graph.unreachable(), ['cycle-a.md', 'cycle-b.md', 'orphan.md'])

    def test_follows_relative_root_encoded_reference_and_html_links(self):
        graph = Graph({'README.md': '[Guide](docs/) [Other][other]\n\n[other]: /OTHER.MD#section\n', 'OTHER.MD': '',
                       'docs/README.md': '[Details](./nested/../a%20b.md?view=1#section)',
                       'docs/a b.md': '<p>See <a href="../end.md">End</a></p>\n', 'end.md': ''})
        self.assertEqual(graph.unreachable(), [])

    def test_ignores_code_images_comments_and_plain_mentions(self):
        content = ('plain.md\n`[Code](inline.md)`\n![Image](image.md)\n'
                   '<!-- [Hidden](comment.md) <a href="comment.md">Hidden</a> -->\n\n'
                   '```markdown\n[Example](fenced.md)\n```\n\n    [Indented](indented.md)\n\n'
                   '<pre><a href="pre.md">Example</a></pre>\n')
        targets = ['comment.md', 'fenced.md', 'image.md', 'indented.md', 'inline.md', 'plain.md', 'pre.md']
        graph = Graph({'README.md': content, **{target: '' for target in targets}})
        self.assertEqual(graph.unreachable(), targets)

    def test_ignores_external_links_anchors_and_paths_outside_repository(self):
        graph = Graph({'README.md': '[Web](https://example.com/remote.md) [Relative web](//example.com/remote.md) '
                                    '[Mail](mailto:remote.md) [File](file:///remote.md) [Anchor](#remote.md) '
                                    '[Outside](../remote.md) [Encoded outside](%2E%2E/remote.md) [Py](script.py)',
                       'remote.md': ''})
        self.assertEqual(graph.unreachable(), ['remote.md'])
        self.assertEqual(graph.missing_targets(['README.md']), {})

    def test_reports_missing_targets_only_for_requested_sources(self):
        graph = Graph({'README.md': '[Index](docs/README.md)',
                       'docs/README.md': '[Deleted](deleted.md) [Renamed](old%20name.md#intro)',
                       'history.md': '[Old evidence](obsolete.md)'})
        self.assertEqual(graph.missing_targets(['README.md', 'docs/README.md']),
                         {'docs/README.md': ['docs/deleted.md', 'docs/old name.md']})


class ExemptionTests(unittest.TestCase):
    def test_directory_prefixes_and_segment_globs(self):
        exempt = coverage.Exemptions(['docs/activities/', '/AGENTS.md', 'skills/*/NOTES.md'])
        self.assertEqual(exempt.filter(['AGENTS.md', 'docs/AGENTS.md', 'docs/activities/2026-x.md', 'docs/activitiesX.md',
                                        'skills/a/NOTES.md', 'skills/a/b/NOTES.md']),
                         ['docs/AGENTS.md', 'docs/activitiesX.md', 'skills/a/b/NOTES.md'])

    def test_third_party_package_internals_are_exempt_but_skill_md_is_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'catalog').mkdir()
            (root / 'catalog/import-manifest.json').write_text(json.dumps({'skills': [
                {'path': 'skills/google/x', 'sourceId': 'google'},
                {'path': 'skills/sufficit/y', 'sourceId': 'sufficit-genius'}]}))
            (root / coverage.IGNORE_FILE).write_text('# comment\n\ndocs/activities/\n')
            exempt = coverage.Exemptions.load(root)
        self.assertEqual(exempt.filter(['skills/google/x/SKILL.md', 'skills/google/x/references/a.md',
                                        'skills/google/xy/a.md', 'skills/sufficit/y/references/b.md',
                                        'docs/activities/z.md']),
                         ['skills/google/x/SKILL.md', 'skills/google/xy/a.md', 'skills/sufficit/y/references/b.md'])


class InventoryTests(unittest.TestCase):
    def test_uses_tracked_and_new_files_excluding_ignored_and_deleted(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            git = lambda *args: subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '--quiet')
            (root / '.gitignore').write_text('ignored.md\n')
            (root / 'README.md').write_text('[New](new.md)')
            (root / 'deleted.md').write_text('')
            git('add', 'README.md', 'deleted.md')
            (root / 'deleted.md').unlink()
            for name in ('new.md', 'ignored.md', 'other.txt'):
                (root / name).write_text('')
            graph = Graph.from_repository(root)
        self.assertEqual(graph.paths(), ['README.md', 'new.md'])
        self.assertEqual(graph.unreachable(), [])

    def test_fails_explicitly_outside_git(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(RuntimeError, 'cannot inventory documentation'):
                Graph.from_repository(Path(temp))


class IndexTests(unittest.TestCase):
    def test_description_handles_block_scalars_and_inert_cells(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp) / 'SKILL.md'
            skill.write_text('---\nname: x\ndescription: >-\n  Uses `code and\n  <tags> | [links](a.md)\nother: y\n---\n')
            text = index.description(skill)
        self.assertEqual(text, 'Uses `code and <tags> | [links](a.md)')
        self.assertEqual(index.markdown_text(text), 'Uses code and &lt;tags> \\| \\[links\\](a.md)')


if __name__ == '__main__':
    unittest.main()
