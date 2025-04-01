import unittest
from scripts.pipeline.database import get_db_path

class TestBasic(unittest.TestCase):
    def test_db_path(self):
        path = get_db_path()
        self.assertTrue(path.endswith("tcga.db"))
        print(f"scussess:{path}")

if __name__ == "__main__":
    unittest.main()