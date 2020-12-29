import unittest
import io
from unittest.mock import patch
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
from converter.utils import allowed_file, copy_file_and_remove, get_content


class TestUtilModule(unittest.TestCase):

    def test_allowed_file_wrong_extension_url(self):
        params = ['http://example.com/test.epub', 'https://example.com/test1.doc']
        for filename in params:
            self.assertFalse(allowed_file(filename), "extension is not allowed should return False")

    def test_allowed_file_true_extension_url(self):
        params = ['http://example.com/test.md', 'https://example.com/test.rtf']
        for filename in params:
            self.assertTrue(allowed_file(filename), "extension is not allowed should return False")

    def test_allowed_file_true_file_extension_(self):
        params = ['test.md', 'test.rtf']
        for filename in params:
            self.assertTrue(allowed_file(filename), f"{filename} should be allowed but fail")

    def test_allowed_file_invalid_file_extension(self):
        params = ['test.doc', 'test.pdf']
        for filename in params:
            self.assertFalse(allowed_file(filename), f"{filename} is not allowed")

    @patch('converter.utils.io.BytesIO')
    @patch('converter.utils.os.remove')
    @patch('converter.utils.open')
    def test_copy_file_and_remove(self, mock_context, mock_remove, mock_bytes):
        mock_bytes = io.BytesIO(b'ok')
        filename = 'somefile.test'
        self.assertEqual(copy_file_and_remove(filename), mock_bytes)
        mock_context.assert_called_once()
        mock_remove.assert_called_once_with(filename)

    @patch('converter.utils.allowed_file')
    @patch('converter.utils.generate_new_name')
    @patch('converter.utils.process_object')
    def test_get_content_file(self, mock_process, mock_gen_new_name, mock_allowed_file):
        builder = EnvironBuilder(method='POST',
                                 data={
                                     'formatList': 'epub',
                                     'file': (io.BytesIO('my file contents'.encode("utf8")), 'test.md')
                                      }
                                 )
        env = builder.get_environ()
        req = Request(env)
        mock_process.return_value = b'my file contents'
        mock_gen_new_name.return_value = 'test.epub'
        file = req.files.get('file')
        mock_allowed_file.return_value = True
        url = None
        self.assertEqual(get_content(req), (b'my file contents', 'test.epub'))
        mock_process.assert_called_once_with(file, url)
        mock_gen_new_name.assert_called_once_with(file.filename, req.form.get('formatList'))
        mock_allowed_file.assert_called_once_with(file.filename)

    @patch('converter.utils.allowed_file')
    @patch('converter.utils.generate_new_name')
    @patch('converter.utils.process_object')
    def test_get_content_url(self, mock_process, mock_gen_new_name, mock_allowed):
        builder = EnvironBuilder(method='POST',
                                 data={
                                     'formatList': 'epub',
                                     'url': 'http:\\example.com'
                                      }
                                 )
        env = builder.get_environ()
        req = Request(env)
        mock_process.return_value = r'http:\\example.com'
        mock_gen_new_name.return_value = 'test.epub'
        mock_allowed.return_value = True
        url = req.form.get('url')
        file = None
        self.assertEqual(get_content(req), (r'http:\\example.com', 'test.epub'))
        mock_process.assert_called_once_with(file, url)
        mock_gen_new_name.assert_called_once_with(url, req.form.get('formatList'))
        mock_allowed.assert_called_once_with(url)
