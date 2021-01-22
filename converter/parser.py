import io
from pathlib import Path
import tempfile
import panflute
from typing import List
import urllib.request
import os
from pypandoc import convert_file
from converter.converter_to_pdf import convert
from converter.github_client.github_client_cls import ConvGitHub, Content


def prepare_book_chp(url: str):
    """Prepare all book chapters for joining"""
    tmpdir = tempfile.mkdtemp()
    get_files(url, tmpdir)
    path_index_chap = find_path_to_chapter(tmpdir, 'index.md')
    chap_lst = create_chapters_lst(path_index_chap)
    chap_lst = [chp.url for chp in chap_lst]
    chap_lst.insert(0, 'index.md')
    return chap_lst, tmpdir


def join_files(links: List[str], dirname: str, fname: str):
    """ Writing all files in one temp """
    with tempfile.NamedTemporaryFile(mode='a+b', suffix='.md') as tmp:
        for i in links:
            path = find_path_to_chapter(dirname, i)
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
    abs_path = next(Path(dirname).rglob(filename))
    abs_path = abs_path.absolute()
    return str(abs_path)


def get_files(url: str, path_on_disc: str) -> None:
    """ Preparing for downloading needed files"""
    g = ConvGitHub()
    repo_content = g.get_content(url, get_doc_source_root())
    for cont in repo_content:
        download_file(cont, path_on_disc)


def download_file(cont_file: Content, path_on_disc: str) -> str:
    """Download files by links"""
    with urllib.request.urlopen(cont_file.download_url) as conn:
        path = os.path.join(path_on_disc, cont_file.name)
        with open(path, 'wb') as file:
            file.write(conn.read())
    return path


def get_doc_source_root():
    return 'doc_source'
