
import requests
from pprint import pprint

class ProfileReader:
    api_url = 'https://api.vk.com/method/'
    base_params = {}

    def __init__(self, token):
        self.base_params = {'access_token': token, 'v': 5.131}

    def resolve_screen_name(self, screen_name: str):
        url = self.api_url + 'utils.resolveScreenName'
        params = {**self.base_params, 'screen_name': screen_name}
        try:
            resp = requests.get(url, params)
            if resp.status_code != 200:
                pprint(resp.text)
            else:
                res = resp.json()
                return res['response']['object_id']

        except Exception as err:
            print(f'error: {err.response.content}')

    def likes_count(self, owner_id: int, item_id: int):
        url = self.api_url + 'likes.getList'
        params = {**self.base_params, 'type': 'photo', 'owner_id': owner_id, 'item_id': item_id}
        try:
            resp = requests.get(url, params)
            if resp.status_code == 200:
                return resp.json()['response']['count']

        except Exception as err:
            print(f'error: {err.response.content}')

    def get_profile_photos(self, owner_id: int):
        url = self.api_url + 'photos.get'
        params = {**self.base_params, 'owner_id': owner_id, 'album_id': 'profile'}
        try:
            resp = requests.get(url, params)
            if resp.status_code != 200:
                pprint(resp.text)
            else:
                photos = []
                res = resp.json()
                for photo in res['response']['items']:
                    bigest_photo = photo['sizes'][len(photo['sizes'])-1]
                    info = {'date': photo['date'], 'id': photo['id'], 'post_id': photo['post_id'],
                            'url': bigest_photo['url'], 'height': bigest_photo['height'], 'width': bigest_photo['width']}
                    likes_count = self.likes_count(owner_id, info['id'])
                    if likes_count is None:
                        return None
                    info['likes_count'] = likes_count
                    photos.append(info)

                return photos

        except Exception as err:
            print(f'error: {err.response.content}')



