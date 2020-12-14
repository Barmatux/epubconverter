from converter.utils import allowed_file, get_mimetype
import pytest
from unittest.mock import Mock


@pytest.mark.parametrize('some_object', ['test.epub', 'test1.doc', 'test2.test'])
def test_wrong_extension_url_allowed_file(some_object):
    assert allowed_file(some_object) is False, "extension is not allowed should return False"


@pytest.mark.parametrize('some_object', ['test.md', 'test.rtf'])
def test_true_extension_url_allowed_file(some_object):
    assert allowed_file(some_object) is True, "Extension is allowed should return True"


@pytest.fixture(params=['test.md', 'test.rtf'], scope='module')
def some_obj(request):
    mock = Mock()
    mock.filename = request.param
    return mock


def test_file_extension_allowed_file(some_obj):
    assert allowed_file(some_obj) is True


@pytest.fixture(params=['test.doc', 'test.pdf'], scope='module')
def some_obj2(request):
    mock = Mock()
    mock.filename = request.param
    return mock


def test_file_extension_false_allowed_file(some_obj2):
    assert allowed_file(some_obj2) is False


@pytest.fixture
def some_obj3():
    mock = Mock()
    return mock


def test_none_allowed_file(some_obj3):
    with pytest.raises(TypeError):
        allowed_file(some_obj3)


@pytest.mark.parametrize('filename, expected', [('test.doc', 'doc'), ('test.md', 'md'), ('test', 'test')])
def test_extends_get_mimetype(filename, expected):
    assert get_mimetype(filename) == expected


@pytest.mark.parametrize('filename', [None, 4, []])
def test_exception_get_mimetype(filename):
    with pytest.raises(AttributeError):
        get_mimetype(filename)
