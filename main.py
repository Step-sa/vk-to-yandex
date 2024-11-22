import requests
import json


def write_to_json(useful_info):
    file = open("test.json", 'w')
    json.dump(useful_info, file)
    file.close()


class VK:

    def __init__(self, access_token, user_id, version='5.199'):

        self.token = access_token

        self.id = user_id

        self.version = version
        self.url = 'https://api.vk.com/method/photos.get'

        self.params = {'access_token': self.token, 'v': self.version}
        self.useful_info = dict()

    def to_yandex(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        path = '/test'

        with open('token.txt') as f:
            token = f.readline()

        headers = {"Authorization": token}

        for key in self.useful_info.keys():
            path = f'/test/{key}'
            img_url = self.useful_info[key]

            response = requests.get(url, params={'path': path}, headers=headers)
            upload_url = response.json()['href']

            response = requests.get(img_url)
            img = response.content

            response = requests.put(upload_url, files={'file': img})
            print(response.status_code)

        response = requests.get(url, params={'path': '/test/j.json'}, headers=headers)
        upload_url = response.json()['href']
        file = open('test.json', 'rb')
        response = requests.put(upload_url, files={'file': file})
        print(response.status_code)
        file.close()

    def get_users_photo(self):
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1,  'photo_sizes': 1}
        response = requests.get(self.url, params={**params, **self.params}).json()
        length = response['response']['count']

        for i in range(length):
            photo_url = response['response']['items'][i]['sizes'][-1]['url']
            likes = str(response['response']['items'][i]['likes']['count'])
            date = str(response['response']['items'][i]['date'])
            name = likes + '.jpg'
            if name not in self.useful_info.keys():
                self.useful_info[name] = photo_url
            else:
                name = likes + date + '.jpg'
                self.useful_info[name] = photo_url

        write_to_json(self.useful_info)


user_id = '391379439'
access_token = ('vk1.a.PXewmBmuyNbX_RzEEmrX4q_87BL1pjivjOArBC6jZ8uwUBz_kCcIb9S6niNc9-NJ48y6nCNECG21BbIER5n9qy9eIsJRR'
                'Ft5KNM4yR5jJyBr5RrB3hp8OEmQfJ2YmEf-U5vEB6DbOKINxq6f4XPamJgWDsK-KKO6OXDaTnY-OqPoeA4CZ5K4C5TRAuUEZfoO')
vk = VK(access_token, user_id)
vk.get_users_photo()

vk.to_yandex()
