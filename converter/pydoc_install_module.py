import shutil
from pypandoc.pandoc_download import download_pandoc


def install_pandoc():
    pandoc = shutil.which('pandoc')
    if not pandoc:
        try:
            download_pandoc()
        except Exception as e:
            print(f'Can\'t install because of {e}')
