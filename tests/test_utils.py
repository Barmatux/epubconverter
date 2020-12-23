import unittest
import io
from unittest.mock import MagicMock, patch
from converter.utils import allowed_file, copy_file_and_remove



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

    def test_allowed_file_invalid_file_extension(self):
        params = ['test.doc', 'test.pdf']
        for filename in params:
            mock = MagicMock()
            mock.filename = filename
            self.assertFalse(allowed_file(mock), f"{filename} is not allowed")

    @patch('converter.converter_2_pdf.generate_new_name')
    @patch('converter.converter_2_pdf.process_file')
    @patch('flask.request')
    def test_get_content(self, request_mock, process_mock, new_name_mock):
        pass

    @patch('converter.utils.io.BytesIO')
    @patch('converter.utils.os.remove')
    @patch('converter.utils.open')
    def test_copy_file_and_remove(self, mock_context, mock_remove, mock_bytes):
        mock_bytes = io.BytesIO(b'ok')
        filename = 'somefile.test'
        self.assertEqual(copy_file_and_remove(filename), mock_bytes)
        mock_context.assert_called_once()
        mock_remove.assert_called_once_with(filename)

