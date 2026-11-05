import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("catalog_versions", Path(__file__).parents[1] / "scripts/catalog_versions.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogVersionTests(unittest.TestCase):
    def test_declared_metadata_and_prerelease(self):
        self.assertEqual("1.2.3-rc.1", module.declared_version('---\nname: demo\nmetadata:\n  version: "1.2.3-rc.1"\n---\nBody'))

    def test_missing_version_is_not_inferred_from_body_or_description(self):
        self.assertIsNone(module.declared_version('---\nname: demo\ndescription: Version 2.0\n---\nversion: 3.0.0'))
        self.assertIsNone(module.declared_version('version: 4.0.0'))
