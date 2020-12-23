from pypandoc.pandoc_download import download_pandoc
import shutil


def install_pandoc():
    pandoc = shutil.which('pandoc')
    if not pandoc:
        download_pandoc()
