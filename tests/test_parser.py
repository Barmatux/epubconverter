import unittest
from unittest.mock import patch, MagicMock
from panflute import Link, elements
from converter.parser import find_path_to_chapter, prepare_book_chp,\
    join_files, create_chapters_lst, get_files


class TestParser(unittest.TestCase):
    @patch('converter.parser.Path')
    def test_find_path_to_chapter_default(self, mock_path):
        res_mock = mock_path.return_value.rglob.return_value. \
            __next__.return_value.absolute.return_value
        actual_result = find_path_to_chapter('some_path', 'index.md')
        self.assertEqual(actual_result, str(res_mock))
        mock_path.assert_called_once_with('some_path')
        mock_path.return_value.rglob.assert_called_once_with('index.md')
        mock_path.return_value.rglob.return_value. \
            __next__.return_value.absolute.assert_called_once()

    @patch('tempfile.mkdtemp')
    @patch('converter.parser.create_chapters_lst')
    @patch('converter.parser.find_path_to_chapter')
    @patch('converter.parser.get_files')
    def test_prepare_book_chp(self, mock_get_files, mock_fpath,
                              mock_book_tree, mock_tempdir):
        mock_tempdir.return_value = 'some_dir_name'
        mock_fpath.return_value = 'some_path'
        mock_book_tree.return_value = [Link(), Link()]
        url = 'some_url'
        prepare_book_chp(url)
        mock_get_files.assert_called_once_with(url, mock_tempdir.return_value)
        mock_tempdir.assert_called_once()
        mock_fpath.assert_called_once_with(mock_tempdir.return_value,
                                           'index.md')
        mock_book_tree.assert_called_once_with(mock_fpath.return_value)

    @patch('converter.parser.convert')
    @patch('converter.parser.open')
    @patch('converter.parser.find_path_to_chapter')
    @patch('tempfile.NamedTemporaryFile')
    def test_join_files(self, mock_temp, mock_path_tfile,
                        mock_open, mock_convert):
        filename = 'test.epub'
        links = ['link', 'link2']
        mock_temp.return_value.__enter__.return_value.name = 'some_file'
        temp_name = mock_temp.return_value.__enter__.return_value.name
        mock_path_tfile.return_value = ['first_file', 'second_file']
        mock_open.return_value.__enter__.return_value.read.return_value = b'ok'
        join_files(links, temp_name, filename)
        mock_temp.assert_called_once()
        mock_convert.assert_called_once_with(temp_name, filename)

    @patch('panflute.run_filter')
    @patch('panflute.load')
    @patch('converter.parser.convert_file')
    def test_create_chapters_lst(self, mock_convert_fl, mock_panflute_load,
                                 mock_run_fltr):
        sources = 'D:\\source.md'
        mock_convert_fl.return_value = 'name : link'
        mock_panflute_load.return_value = elements.Doc()
        mock_run_fltr.return_value = elements.Doc()
        mock_doc = mock_run_fltr.return_value
        mock_doc.chapters = []
        create_chapters_lst(sources)
        mock_convert_fl.assert_called_once()
        mock_run_fltr.assert_called_once()
        mock_panflute_load.assert_called_once()

    @patch('converter.parser.download_file')
    @patch('converter.parser.ConvGitHub')
    def test_get_files(self, mock_cls_inst, mock_download):
        cont = MagicMock()
        mock_cls_inst.return_value.get_content.return_value = [cont]

        get_files('some_url', 'some_path')

        mock_cls_inst.assert_called_once()
        mock_download.assert_called_once_with(cont, 'some_path')
