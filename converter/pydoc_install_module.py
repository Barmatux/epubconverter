from pypandoc.pandoc_download import download_pandoc
import shutil


def install_pandoc():
    pandoc = shutil.which('pandoc')
    if pandoc:
        print(f' Path to {pandoc}')
        return 1
    else:
        try:
            download_pandoc()
            return 1
        except Exception as e:
            print(f'Can\'t install because of {e}')
            return -1
