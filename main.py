import operator

import vk_api
import yadisk_api
from pprint import pprint
import requests

def read_token(file_path: str):
    with open(file_path) as f:
        return f.readline()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    vk_token = read_token('vk_token.txt')
    vk_reader = vk_api.ProfileReader(vk_token)

    # Входящие параметры
    vk_screen_name = input('Укажите screen name пользователя VK (например, begemot_korovin):');
    if vk_screen_name == '':
        vk_screen_name = 'begemot_korovin'

    yad_token = input('Укажите токен Яндекс.Диска:');
    yad_token = read_token('yadisk_token.txt')

    max_number_str = input('Укажите количество выгружаемых фото (5 по умолчанию):');
    if max_number_str == '':
        max_number_of_photos = 5
    else:
        max_number_of_photos = int(max_number_str)

    vk_id = vk_reader.resolve_screen_name(vk_screen_name)
    if vk_id != None:

        # Получаем фото
        photos = vk_reader.get_profile_photos(vk_id)
        sorted_photos = sorted(photos, key=operator.itemgetter('height', 'width'), reverse=True)

        # Подключаемся к диску, создаем каталог и очищаем его (удаляем все предыдущие фото)
        ya_disk = yadisk_api.YaDisk(yad_token)
        if ya_disk.create_folder(vk_screen_name) == True:
            names = []
            files_info = []
            for i in range(min(max_number_of_photos, len(sorted_photos))):
                file_name = str(sorted_photos[i]['likes_count'])
                if file_name in names:
                    file_name += '_' + sorted_photos[i].date
                else:
                    names.append(file_name)

                file_name += '.jpg'
                files_info.append({'file_name': file_name, 'size': f"{sorted_photos[i]['height']}x{sorted_photos[i]['width']}"})

                resp = requests.get(sorted_photos[i]['url'], allow_redirects=True)
                with open('temp.tmp', 'wb') as file:
                    file.write(resp.content)

                if ya_disk.upload('temp.tmp', f'{vk_screen_name}/{file_name}') != True:
                    break

            pprint(files_info)


