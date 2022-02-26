import unittest

import requests

from yadisk import YaDiskMkDir

class TestCreateDirOnYaDisk(unittest.TestCase):
    def setUp(self) -> None:
        with open('token.txt') as file:
            self.token = file.readline().strip()
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        self.path = 'TestDir'
        self.params = {'path': self.path}

    def tearDown(self) -> None:
        requests.delete(
            self.url,
            headers=self.headers,
            params=self.params
        )

    def test_create_dir(self):
        response = requests.put(
            self.url,
            headers=self.headers,
            params=self.params
        )
        self.assertEqual(response.status_code, 201)

    def test_create_dir_already_exist(self):
        requests.put(
            self.url,
            headers=self.headers,
            params=self.params
        )
        response = requests.put(
            self.url,
            headers=self.headers,
            params=self.params
        )
        self.assertEqual(response.status_code, 409)

    def test_create_dir_wrong_token(self):
        headers = {
            'Content-type': 'application/json',
            'Authorization': f'OAuth TOKEN',
        }
        response = requests.put(
            self.url,
            headers=headers,
            params=self.params
        )
        self.assertEqual(response.status_code, 401)

    def test_create_dir_incorrect_params(self):
        params = {'paths': self.path}
        response = requests.put(
            self.url,
            headers=self.headers,
            params=params
        )
        self.assertEqual(response.status_code, 400)

    def test_create_dir_incorrect_headers(self):
        self.url += 'wrong/'
        response = requests.put(
            self.url,
            headers=self.headers,
            params=self.params
        )
        self.assertEqual(response.status_code, 405)
