import unittest
from converter.converter_2_pdf import _change_name, _read_stream, convert_to_user_format, convert
from unittest.mock import MagicMock, patch
import io


class TestConvertedToPdfFunctions(unittest.TestCase):

    def test_change_name_url_input(self):
        url = ['https://example.com/test.md', 'http://example.ru/test/test.html']
        output_format = ['epub', 'rtf']
        expected = ['test.epub', 'test.rtf']
        for ur, out_f, exp in zip(url, output_format, expected):
            res = _change_name(ur, out_f)
            self.assertEqual(res, exp, f"Name should be {exp}, but got {res}")

    def test_change_name_wrong_input(self):
        url = ['https://example.com/test', 'http://example.com/test/test#somtehing=1?']
        output_format = [None, 1]
        for ur, out_f in zip(url, output_format):
            with self.assertRaises(TypeError):
                _change_name(ur, out_f)

    def test_file_change_name(self):
        mock_file = MagicMock()
        mock_file.filename = 'test.md'
        output_format = ['epub', 'rtf']
        expected = ['test.epub', 'test.rtf']
        for out_f, exp in zip(output_format, expected):
            res = _change_name(mock_file, out_f)
            self.assertEqual(res, exp, f'Waiting for {exp} but got {res}')

    def test_read_stream_from_file(self):
        mock_text = MagicMock()
        mock_text.stream = io.StringIO('Read done')
        self.assertEqual(_read_stream(mock_text), 'Read done')

    @patch('urllib.request.urlopen')
    def test_read_stream_from_url(self, mock):
        mock.return_value.__enter__.return_value.read.return_value = 'ok'
        test_url = 'http:\\example.com'
        self.assertEqual(_read_stream(test_url), 'ok')
        mock.assert_called_with(test_url)

    @patch('converter.converter_2_pdf.convert')
    @patch('converter.converter_2_pdf._read_stream')
    def test_convert_to_user_format(self, mock_read_stream, mock_convert):
        mock_read_stream.return_value = b'some.txt'
        mock_convert.return_value = 'name.epub'
        assert convert_to_user_format(r'D:\test.md', 'format') == 'name.epub'
        mock_read_stream.assert_called_once_with(r'D:\test.md')
        mock_convert.assert_called_once()

    @patch('os.replace', return_value='result.epub')
    @patch('converter.converter_2_pdf.convert_file')
    @patch('converter.converter_2_pdf._change_name')
    def test_convert(self, mock_change_name, mock_convert, mock_replace):
        mock_change_name.return_value = 'test.epub'
        assert convert('some_path', 'new_path', 'epub') == 'test.epub'
        mock_change_name.assert_called_once()
        mock_convert.assert_called_once()
