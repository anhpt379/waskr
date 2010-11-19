from waskr import util
import unittest

class TestRequestParser(unittest.TestCase):
    
    def test_init(self):
        rp = util.RequestParser(config={}, test=True)

        self.assertEqual(rp.config, {})
        self.assertEqual(rp.cache, [])

    def test_construct_no_len(self):
        rp = util.RequestParser(config={'cache':2}, test=True)
        rp.construct('foo')
        actual = rp.cache[0]
        expected = 'foo'
        self.assertEqual(actual, expected) 
        self.assertEqual(len(rp.cache), 1)

    def test_flush(self):
        rp = util.RequestParser(config={'cache':1}, test=True)
        rp.cache = ['foo']
        actual = rp.cache[0]
        expected = 'foo'
        
        self.assertEqual(actual, expected) 
        self.assertEqual(len(rp.cache), 1)

        rp.flush()

        self.assertEqual(rp.cache, [])

    
