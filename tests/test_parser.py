import unittest
from unittest.mock import patch
from pathlib import Path
from panflute import Link, elements
from converter.parser import find_path_to_file, create_one_file_from_many,\
    create_and_convert, create_book_tree


class TestParser(unittest.TestCase):

    @patch('converter.parser.Path.as_posix')
    @patch('converter.parser.Path.rglob')
    def test_find_path_to_file_default(self, mock_path, mock_as_posix):
        mock_path.return_value = [Path('D:\\')]
        mock_as_posix.return_value = 'D:\\index.md'
        self.assertEqual(find_path_to_file('D:\\'), 'D:\\index.md')
        mock_path.assert_called_once()
        mock_as_posix.assert_called_once()

    @patch('tempfile.TemporaryDirectory')
    @patch('converter.parser.create_and_convert')
    @patch('converter.parser.create_book_tree')
    @patch('converter.parser.find_path_to_file')
    @patch('converter.parser.clone_repository')
    def test_create_one_file_from_many(self, mock_clone_rp, mock_fpath,
                                       mock_book_tree, mock_cr_and_conv,
                                       mock_tempdir):
        mock_tempdir.return_value.__enter__.return_value = 'some_dir_name'
        mock_fpath.return_value = 'D:\\'
        mock_book_tree.return_value = ['D:\\test\\test', ]
        temp_dir = mock_tempdir.return_value.__enter__.return_value
        url = 'some_url'
        filename = 'somefile.md'
        create_one_file_from_many(url, filename)
        mock_clone_rp.assert_called_once_with(url, temp_dir)
        mock_tempdir.assert_called_once()
        mock_fpath.assert_called_once_with(temp_dir)
        mock_book_tree.assert_called_once_with(mock_fpath.return_value)
        mock_cr_and_conv.assert_called_once_with(mock_book_tree.return_value,
                                                 temp_dir, filename)

    @patch('converter.parser.convert')
    @patch('converter.parser.open')
    @patch('converter.parser.find_path_to_file')
    @patch('tempfile.NamedTemporaryFile')
    def test_create_and_convert(self, mock_temp, mock_path_tfile,
                                mock_open, mock_convert):
        filename = 'test.epub'
        links = [Link(), Link()]
        mock_temp.return_value.__enter__.return_value.name = 'some_file'
        temp_name = mock_temp.return_value.__enter__.return_value.name
        mock_path_tfile.return_value = ['first_file', 'second_file']
        mock_open.return_value.__enter__.return_value.read.return_value = b'ok'
        create_and_convert(links, temp_name, filename)
        mock_temp.assert_called_once()
        mock_convert.assert_called_once_with(temp_name, filename)

    @patch('panflute.run_filter')
    @patch('panflute.load')
    @patch('converter.parser.convert_file')
    def test_create_book_tree(self, mock_convert_fl, mock_panflute_load,
                              mock_run_fltr):
        sources = 'D:\\source.md'
        mock_convert_fl.return_value = 'name : link'
        mock_panflute_load.return_value = elements.Doc()
        mock_run_fltr.return_value = elements.Doc()
        mock_doc = mock_run_fltr.return_value
        mock_doc.links = []
        create_book_tree(sources)
        mock_convert_fl.assert_called_once()
        mock_run_fltr.assert_called_once()
        mock_panflute_load.assert_called_once()
