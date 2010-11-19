import unittest

"""Make sure we are able to import everything we need for waskr"""


class TestImportDependencies(unittest.TestCase):

    def test_import_bottle(self):
        "Import Bottle"
        try:
            import bottle
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_nose(self):
        "Import Nose"
        try:
            import nose
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_pymongo(self):
        "Import pymongo"
        try:
            import pymongo
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


if __name__ == '__main__':
    unittest.main()
