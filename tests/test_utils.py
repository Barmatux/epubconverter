import unittest
from unittest.mock import MagicMock
from converter.utils import allowed_file, get_mimetype


class TestUtilModule(unittest.TestCase):
    def test_allowed_file_wrong_extension_url(self):
        params = ['test.epub', 'test1.doc', 'test2.test']
        for i in params:
            self.assertFalse(allowed_file(i), "extension is not allowed should return False")

    def test_allowed_file_true_extension_url(self):
        params = ['test.md', 'test.rtf']
        for i in params:
            self.assertTrue(allowed_file(i), "extension is not allowed should return False")

    def test_allowed_file_true_file_extension_(self):
        params = ['test.md', 'test.rtf']
        for i in params:
            mock = MagicMock()
            mock.filename = i
            self.assertTrue(allowed_file(mock), "File should be allowed but fail")

    def test_file_extension_invalid_file_extension(self):
        params = ['test.doc', 'test.pdf']
        for i in params:
            mock = MagicMock()
            mock.filename = i
            self.assertTrue(allowed_file(mock), "File should be allowed but fail")

    def test_none_allowed_file(self):
        with self.assertRaises(AttributeError):
            allowed_file(None)

    def test_extends_get_mimetype(self,):
        input_params = ['test.doc', 'test.md']
        output_params = ['doc', 'md']
        for in_param, out_param in zip(input_params, output_params):
            msg = f"Failing while getting mimetype of file. Expected {out_param}"
            self.assertEqual(get_mimetype(in_param), out_param, msg)

    def test_get_mimetype_none(self):
        with self.assertRaises(AttributeError):
            get_mimetype(None)
