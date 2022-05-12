
from pprint import pprint
import requests

class YaDisk:
    def __init__(self, token: str):
        self.token = token

    def get_upload_link(self, path_to_file_on_disk: str):
        href = ''

        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': f"OAuth {self.token}", 'Content-Type': 'application/json'}
        params = {'path': path_to_file_on_disk, 'overwrite': True}

        resp = requests.get(url, params, headers=headers)
        if resp.status_code != 200:
            pprint(resp.text)
        else:
            # {
            #     "operation_id": "string",
            #     "href": "string",
            #     "method": "string",
            #     "templated": true
            # }
            resp_json = resp.json()
            href = resp_json['href']
        return href

    def upload(self, file_path: str, file_path_on_disk: str):
        upload_link = self.get_upload_link(file_path_on_disk)
        if upload_link != "":
            with open(file_path, 'rb') as f:
                resp = requests.put(upload_link, f)
                if resp.status_code == 200 or resp.status_code == 201:
                    return True
                else:
                    print(resp.text)

    def create_folder(self, folder_name):
        url = f'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f"OAuth {self.token}", 'Content-Type': 'application/json'}
        params = {'path': folder_name}

        resp = requests.put(url, params=params, headers=headers)
        if resp.status_code != 201:
            if resp.status_code == 409:
                if resp.json()['error'] == 'DiskPathPointsToExistentDirectoryError':
                    # Каталог был создан ранее, не считаем ошибкой
                    return True
            else:
                pprint(resp.text)
                return False
        else:
            return True




