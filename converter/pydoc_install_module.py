import shutil
from pypandoc.pandoc_download import download_pandoc


def install_pandoc():
    pandoc = shutil.which('pandoc')
    if not pandoc:
        download_pandoc()
