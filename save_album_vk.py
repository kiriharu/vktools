# coding = utf-8
import time
import requests

def call(method, options={}, **kwargs):
    '''Фукнция вызова api ВК.'''
    options['access_token'] = token
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def gethiresphotolink(p):
    '''Получает фото и возвращает ссылку на хайрез'''
    ky = p.keys()
    ak = []
    for k in ky:
        try:
            k.index('photo_')
            ak.append(int(k.replace('photo_', '')))
        except Exception: pass
    return p['photo_%s'%max(ak)]

def get_albums(userid):
    '''Получение photos.getAlbums(списка альбомов) по owner_id'''
    options = {
        'owner_id' : userid
    }
    get_albums_resp = call('photos.getAlbums', options)
    return get_albums_resp

def photos_get(owner_id, albumid):
    '''Получение списка фото по id владельца и id альбома'''
    photos = call('photos.get', owner_id=owner_id, album_id=albumid)['response']['items']
    urls = []
    for pic in photos:
        urls.append(gethiresphotolink(pic))
    return urls

def main():
    '''Главная функция'''
    modeoption = input("Сохранение альбомов ВКонтакте. \n Нажмите 1 чтобы просмотреть ваши альбомы \n Нажмите 2 чтобы начать сохранение всех картинок: ")
    if modeoption == '1':
        print("По дефолту существует 3 служебных альбома: \n wall — фотографии со стены; \n profile — фотографии профиля; \n saved — сохраненные фотографии.")
        #Получаем userid
        myuid = call('users.get', {})['response'][0]['id']
        data_getalbums = get_albums(myuid)['response']['items']
        for data in data_getalbums:
            print('ID пользователя: {0}, ID альбома: {1}, Название альбома: {2} \n'.format(data['owner_id'], data['id'], data['title']))
        main()
    if modeoption == '2':
        albumid = input("Для начала, введите альбом для сохранения: ")
        myuid = call('users.get', {})['response'][0]['id']
        urls = photos_get(myuid, albumid)
        i = 1
        for url in urls:
            name = url.split('/')[-1]
            print('%2s/%2s: %s'%(i, len(urls), name))
            i += 1
            try:
                with open(name, 'wb') as file:
                    data = requests.get(url).content
                    file.write(data)
            except IOError:
                print('Путь не найден или запись в него невозможна')

if __name__ == '__main__':
    token = input("Введите access token: ")
    main()
    print("Введите enter чтобы выйти.")
