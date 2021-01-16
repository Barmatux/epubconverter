import io
from pygit2 import clone_repository
from pathlib import Path
import tempfile
import panflute
from typing import List
from pypandoc import convert_file
from converter.converter_2_pdf import convert


def prepare_book_chp(url: str):
    """Prepare all book chapters for joining"""
    tmpdir = tempfile.mkdtemp()
    clone_repository(url, tmpdir)
    path_index_chap = find_path_to_chapter(tmpdir, 'index.md')
    chap_lst = create_chapters_lst(path_index_chap)
    return chap_lst, tmpdir


def join_files(links: List[panflute.Link], dirname: str, fname: str):
    """ Writing all files in one temp """
    with tempfile.NamedTemporaryFile(mode='a+b', suffix='.md') as tmp:
        for i in links:
            path = find_path_to_chapter(dirname, i.url)
            with open(path, 'rb') as f_r:
                tmp.write(f_r.read())
    convert(tmp.name, fname)


def create_chapters_lst(source: str) -> List[panflute.Link]:
    """Find all links in source file and return list of links to chapters"""
    data = convert_file(source, 'json')
    doc = panflute.load(io.StringIO(data))
    doc.chapters = []

    def action(elem, doc):
        if isinstance(elem, panflute.Link):
            doc.chapters.append(elem)
    doc = panflute.run_filter(action,  doc=doc)
    return doc.chapters


def find_path_to_chapter(dirname: str, filename: str) -> str:
    """Return path by filename """
    abs_path = None
    for path in Path(dirname).rglob(filename):
        abs_path = path.absolute()
    return abs_path.as_posix()
