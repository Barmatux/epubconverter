import unittest
from unittest.mock import MagicMock, patch
import io
from converter.converter_2_pdf import convert_to_user_format, convert, process_content, generate_new_name


class TestConvertedToPdfFunctions(unittest.TestCase):

    def test_process_content_file(self):
        mock = MagicMock()
        mock.stream = io.BytesIO(b'ok')
        self.assertEqual(process_content(file=mock), b'ok')

    @patch('urllib.request.urlopen')
    def test_process_content_url_input(self, mock):
        mock.return_value.__enter__.return_value.read.return_value = 'ok'
        test_url = 'http:\\example.com'
        self.assertEqual(process_content(url=test_url), 'ok')
        mock.assert_called_with(test_url)

    def test_generate_new_name_from_url(self):
        url = ['https://example.com/test.md', 'http://example.ru/test/test.html']
        output_format = ['epub', 'rtf']
        expected = ['test.epub', 'test.rtf']
        for ur, out_f, exp in zip(url, output_format, expected):
            res = generate_new_name(ur, out_f)
            self.assertEqual(res, exp, f"Name should be {exp}, but got {res}")

    def test_generate_new_name(self):
        mock_file = MagicMock()
        mock_file.filename = 'test.md'
        output_format = ['epub', 'rtf']
        expected = ['test.epub', 'test.rtf']
        for out_f, exp in zip(output_format, expected):
            res = generate_new_name(mock_file.filename, out_f)
            self.assertEqual(res, exp, f'Waiting for {exp} but got {res}')

    @patch('tempfile.NamedTemporaryFile')
    @patch('converter.converter_2_pdf.convert')
    def test_convert_to_user_format(self, mock_convert, mock_tmp):
        mock_tmp.return_value.__enter__.return_value.name = 'some_dir_name'
        filename = 'test.epub'
        mock = bytes(b'ok')
        assert convert_to_user_format(mock, filename) == 'test.epub'
        mock_convert.assert_called_once_with('some_dir_name', filename)
        mock_tmp.assert_called_once()

    @patch('converter.converter_2_pdf.convert_file')
    def test_convert(self, mock_convert):
        url_path = 'temp_path'
        new_file_name = 'test.epub'
        convert(url_path, new_file_name)
        mock_convert.assert_called_once_with(url_path, new_file_name.split('.')[-1], outputfile='test.epub')
