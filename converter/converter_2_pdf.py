import pypandoc
import urllib
import os
import time


class Converter:

    def _write_on_disk(self, address: str):
        """Writing file from address to disk"""
        test = os.path.join(os.getcwd(), address.split('/')[-1])
        urllib.request.urlretrieve(address, test)
        return test


    def _make_output_file_name(self, address: str) -> str:
        """Creating the same name as input file, but with .epub suffix"""
        return address.replace(address[-2:], 'epub')

    def convert(self, address: str) -> None:
        """ Return new file name"""
        if address.startswith('https://'):
            address = self._write_on_disk(address)
        pypandoc.convert_file(address, 'epub', outputfile=self._make_output_file_name(address))
        os.remove(address)




if __name__ == '__main__':
    c = Converter()
    c.convert('https://github.com/awsdocs/amazon-athena-user-guide/blob/main/CODE_OF_CONDUCT.md')

    # pypandoc.convert_file(r'D:\JetBrains\PyCharm Community Edition 2020.2.3\jbr\bin\CODE_OF_CONDUCT.md', 'epub', outputfile=r'D:\JetBrains\PyCharm Community Edition 2020.2.3\jbr\bin\test123.epub')