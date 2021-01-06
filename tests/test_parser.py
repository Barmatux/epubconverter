import unittest
from urllib.parse import urlsplit
from converter.parser import get_file_name


class TestParser(unittest.TestCase):
    def test_get_file_name_master(self):
        test_url = r'https://github.com/awsdocs/amazon-vpc-user-guide/' \
                   r'blob/master/CONTRIBUTING.md'
        path_to_file = urlsplit(test_url).path.split('master')[-1]
        test_case = path_to_file.replace('/', '', 1)
        self.assertEqual(get_file_name(test_url), test_case)

    def test_get_file_name_main(self):
        test_url = r'https://github.com/awsdocs/aws-cdk-guide' \
                   r'/blob/main/README.md'
        path_to_file = urlsplit(test_url).path.split('main')[-1]
        test_case = path_to_file.replace('/', '', 1)
        self.assertEqual(get_file_name(test_url), test_case)

    def test_get_file_name_repo(self):
        test_url = r'https://github.com/awsdocs/aws-cdk-guide'
        self.assertEqual(get_file_name(test_url), '')
