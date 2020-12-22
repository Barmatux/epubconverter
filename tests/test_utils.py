import unittest
from unittest.mock import MagicMock, patch, mock_open
import flask
import io
from converter.utils import allowed_file, _get_file_extension, get_content, copy_file_and_remove
from converter.converter_2_pdf import process_file, process_url, generate_new_name


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

    def test_get_file_extension(self):
        input_params = ['test.doc', 'test.md']
        output_params = ['doc', 'md']
        for in_param, out_param in zip(input_params, output_params):
            msg = f"Failing while getting file's extension. Expected {out_param}"
            self.assertEqual(_get_file_extension(in_param), out_param, msg)

    @patch('converter.converter_2_pdf.generate_new_name')
    @patch('converter.converter_2_pdf.process_file')
    @patch('flask.request')
    def test_get_content(self, request_mock, process_mock, new_name_mock):
        pass

    @patch('converter.utils.io.BytesIO')
    @patch('converter.utils.os.remove')
    @patch('converter.utils.open' )
    @patch('converter.utils._get_file_extension')
    def test_copy_file_and_remove(self, mock_get_new_extension, mock_context, mock_remove, mock_bytes):
        mock_get_new_extension.return_value = 'epub'
        # mock_open(read_data=b'ok')
        mock_bytes.return_value.read.return_value = b'ok'
        filename = 'somefile.test'
        self.assertEqual(copy_file_and_remove(filename), ('epub', b'ok'))
        mock_context.assert_called_once()
        mock_get_new_extension.assert_called_once_with(filename)
        mock_remove.assert_called_once_with(filename)
        mock_bytes.assert_any_call()