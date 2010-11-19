import unittest

from waskr  import log


class TestLog(unittest.TestCase):

    def test_middleware(self):
        try:
            log.middleware
            log_instance = True
        except AttributeError:
            log_instance = False
        self.assertTrue(log_instance)


    def test_util(self):
        try:
            log.util
            log_instance = True
        except AttributeError:
            log_instance = False
        self.assertTrue(log_instance)


    def test_database(self):
        try:
            log.database
            log_instance = True
        except AttributeError:
            log_instance = False
        self.assertTrue(log_instance)


    def test_server(self):
        try:
            log.server
            log_instance = True
        except AttributeError:
            log_instance = False
        self.assertTrue(log_instance)


    def test_model(self):
        try:
            log.model
            log_instance = True
        except AttributeError:
            log_instance = False
        self.assertTrue(log_instance)



if __name__ == '__main__':
    unittest.main()
