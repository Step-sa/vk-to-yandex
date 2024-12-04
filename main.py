import requests
import json

def write_to_json(useful_info):
    file = open("test.json", 'w')
    json.dump(useful_info, file)
    file.close()
    print('Был создан json файл')


class VK:

    def __init__(self, access_token, user_id, version='5.199'):

        self.token = access_token

        self.id = user_id

        self.version = version
        self.url = 'https://api.vk.com/method/photos.get'

        self.params = {'access_token': self.token, 'v': self.version}
        self.useful_info = []

    def to_yandex(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

        path = '/img'

        with open('token.txt') as f:
            token = f.readline()
            print('Был получен токен для api Яндекса')

        headers = {"Authorization": token}

        url_to_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.put(url_to_folder, params={'path': path}, headers=headers)
        print('Создание папки на яндекс диске:', response.status_code)

        for key in self.useful_info.keys():
            path = f'/img/{key}'
            img_url = self.useful_info[key]

            response = requests.get(url, params={'path': path}, headers=headers)
            upload_url = response.json()['href']
            print(f'Получена ссылка для загрузки фото {key}: {response.status_code}')

            response = requests.get(img_url)
            img = response.content
            print(f'Получено представление фото {key}: {response.status_code}')

            response = requests.put(upload_url, files={'file': img})
            print(f'Загрузка фото {key}: {response.status_code}')

        response = requests.get(url, params={'path': '/img/j.json'}, headers=headers)
        print(f'Получена ссылка для загрузки json файла {response.status_code}')
        upload_url = response.json()['href']
        file = open('test.json', 'rb')
        response = requests.put(upload_url, files={'file': file})
        file.close()
        print(f'Загрузка json файла: {response.status_code}')

    def get_users_photo(self):
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1,  'photo_sizes': 1, 'count': 5}
        response = requests.get(self.url, params={**params, **self.params})
        data = response.json()
        print(f'Получены фото пользователя: {response.status_code}')
        length = params['count']
        for i in range(length):
            useful_info = dict()
            photo_url = data['response']['items'][i]['sizes'][-1]['url']
            likes = str(data['response']['items'][i]['likes']['count'])
            date = str(data['response']['items'][i]['date'])
            size = (str(data['response']['items'][i]['sizes'][-1]['height']) +
                    str(data['response']['items'][i]['sizes'][-1]['width']))
            print('Получены данные о фото: ', i + 1)
            name = likes + '.jpg'
            if name not in useful_info.keys():
                useful_info["name"] = name
            else:
                name = likes + date + '.jpg'
                useful_info["name"] = name
            print('Создано уникальное имя для файла: ', i + 1)
            useful_info['size'] = size
            self.useful_info.append(useful_info)

        write_to_json(self.useful_info)


user_id = '391379439'
access_token = ('vk1.a.h22l54VOPG3DMAO06oU67OI32eJMgvYN9jtbHygquQlrlwtMky-DFtbHmA6W5Nt631Q_SxZuamAM_r0hCLnFcalrYrElI5J'
                'HEjvQAGQL9gFWHECG4YaRWQhLqkl03WCO1fQ2xtEa0D5mZCp_B_NeUoktPCSkhS1Z23FNZ3g348-j10Z1rc_WcunpCxyv-9hh')
vk = VK(access_token, user_id)
vk.get_users_photo()
vk.to_yandex()