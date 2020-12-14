from converter.converter_2_pdf import _change_name, _read_stream, convert_to_user_format, convert
import pytest
from unittest.mock import Mock, patch
import io


@pytest.mark.parametrize('url, output_format, expected', [('https://example.com/test.md', 'epub', 'test.epub'),
                                                          ('http://example.ru/test/test.html', 'rtf', 'test.rtf'),
                                                          ]
                         )
def test_url_change_name(url, output_format, expected):
    assert _change_name(url, output_format) == expected


@pytest.mark.parametrize('url, output_format', [('https://example.com/test', None),
                                                ('http://example.com/test/test#somtehing=1?', 1),
                                                ]
                         )
def test_wrong_url_change_name(url, output_format):
    with pytest.raises(TypeError):
        _change_name(url, output_format)


@pytest.fixture
def file_storage_mock():
    test_file = Mock()
    test_file.filename = 'test.md'
    return test_file


@pytest.mark.parametrize('output_format, expected', [('epub', 'test.epub'), ('rtf', 'test.rtf')])
def test_file_change_name(file_storage_mock, output_format, expected):
    assert _change_name(file_storage_mock, output_format) == expected


def test_file_read_stream():
    mock = Mock()
    mock.stream = io.StringIO('Read done')
    assert _read_stream(mock) == 'Read done'


def test_url_file_read_stream(mocker):
    test_url = 'http:\\example.com'
    mocker.patch('urllib.request.urlopen').return_value.__enter__.return_value.read.return_value = 'ok'
    assert _read_stream(test_url) == 'ok'


@patch('converter.converter_2_pdf.convert')
@patch('converter.converter_2_pdf._read_stream')
def test_convert_to_user_format(mock_read_stream, mock_convert):
    mock_read_stream.return_value = b'some.txt'
    mock_convert.return_value = 'name.epub'
    assert convert_to_user_format(r'D:\test.md', 'format') == 'name.epub'
    mock_read_stream.assert_called_once_with(r'D:\test.md')
    mock_convert.assert_called_once()


@patch('os.replace', return_value='result.epub')
@patch('converter.converter_2_pdf.convert_file')
@patch('converter.converter_2_pdf._change_name')
def test_convert(mock_change_name, mock_convert, mock_replace):
    mock_change_name.return_value = 'test.epub'
    assert convert('some_path', 'new_path', 'epub') == 'test.epub'
    mock_change_name.assert_called_once()
    mock_convert.assert_called_once()
