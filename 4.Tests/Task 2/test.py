import unittest
import requests


class TestCreateDirOnYaDisk(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('token.txt') as file:
            cls.token = file.readline().strip()
        cls.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        cls.headers = {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {cls.token}'
        }
        cls.path = 'TestDir'
        cls.params = {'path': cls.path}

    @classmethod
    def tearDownClass(cls) -> None:
        requests.delete(
            cls.url,
            headers=cls.headers,
            params=cls.params
        )

    def test_create_dir(self):
        response = requests.put(
            self.url,
            headers=self.headers,
            params=self.params
        )
        self.assertEqual(response.status_code, 201)

    def test_create_dir_already_exist(self):
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
