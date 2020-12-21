import unittest
from unittest.mock import MagicMock
from converter.utils import allowed_file, get_mimetype


class TestUtilModule(unittest.TestCase):
    def test_allowed_file_wrong_extension_url(self):
        params = ['test.epub', 'test1.doc', 'test2.test', 'test']
        for filename in params:
            self.assertFalse(allowed_file(filename), "extension is not allowed should return False")

    def test_allowed_file_true_extension_url(self):
        params = ['test.md', 'test.rtf']
        for filename in params:
            self.assertTrue(allowed_file(filename), "extension is not allowed should return False")

    def test_allowed_file_true_file_extension_(self):
        params = ['test.md', 'test.rtf']
        for filename in params:
            mock = MagicMock()
            mock.filename = filename
            self.assertTrue(allowed_file(mock), f"{filename} should be allowed but fail")

    def test_file_extension_invalid_file_extension(self):
        params = ['test.doc', 'test.pdf']
        for filename in params:
            mock = MagicMock()
            mock.filename = filename
            self.assertFalse(allowed_file(mock), f"{filename} is not allowed")

    def test_extends_get_mimetype(self,):
        input_params = ['test.doc', 'test.md']
        output_params = ['doc', 'md']
        for in_param, out_param in zip(input_params, output_params):
            msg = f"Failing while getting mimetype of file. Expected {out_param}"
            self.assertEqual(get_mimetype(in_param), out_param, msg)
