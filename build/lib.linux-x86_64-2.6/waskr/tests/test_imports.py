import unittest

"""Make sure we are able to import everything from waskr"""


class TestImports(unittest.TestCase):

    def test_import_waskr(self):
        try:
            import waskr
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_database(self):
        try:
            from  waskr import database
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_middleware(self):
        try:
            from waskr import middleware
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_RequestStatsMiddleware(self):
        try:
            from waskr.middleware import RequestStatsMiddleware
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_util(self):
        try:
            from waskr import util
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_web(self):
        try:
            from waskr import web
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_server(self):
        try:
            from waskr.web import server
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_db_stats(self):
        try:
            from waskr.database  import Stats
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_Synchronizer(self):
        try:
            from waskr.util  import Synchronizer
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_RequestParser(self):
        try:
            from waskr.util  import Synchronizer
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_util_config(self):
        try:
            from waskr  import config
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)


    def test_import_util_config_options(self):
        try:
            from waskr.config import options 
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)

    def test_import_log(self):
        try:
            from waskr  import log
            imported = True
        except ImportError:
            imported = False
        self.assertTrue(imported)



if __name__ == '__main__':
    unittest.main()
