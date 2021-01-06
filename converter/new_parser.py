from github import Github
import urllib.request
import io
from pygit2 import clone_repository
from pathlib import Path
import tempfile
import panflute
import pypandoc


def clone_repo(input_path):
    clone_repository(r'https://github.com/awsdocs/amazon-ec2-user-guide', input_path)


def create_temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        clone_repo(tmpdirname)
        index_path = find_path_to_file(tmpdirname)
        lnks_lst = create_book_tree(index_path)
        for i in lnks_lst:
            path = find_path_to_file(tmpdirname, i.url)
            with open('D:\\test.md', 'ab') as f_w:
                print(path)
                with open(path, 'rb') as f_r:
                    f_w.write(f_r.read())


def create_book_tree(source) -> list[panflute.Link]:
    data = pypandoc.convert_file(source, 'json')
    doc = panflute.load(io.StringIO(data))
    doc.links = []
    doc = panflute.run_filter(action,  doc=doc)
    return doc.links


def find_path_to_file(dirname, filename='index.md') -> str:
    p = None
    for path in Path(dirname).rglob(filename):
        p = path.absolute()
    return p.as_posix()


def action(elem, doc):
    if isinstance(elem, panflute.Link):
        doc.links.append(elem)


if __name__ == '__main__':
    create_temp_dir()

