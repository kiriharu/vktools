#Легендарный byebyevk. Лучше посмотрите тут - https://github.com/asylumone/bye-bye-vk, там он более прокачан. Требует requests и time.
import requests, time
from pprint import pprint

def call(method, options={}, **kwargs):
    '''Функция вызова api VK'''
    options['access_token'] = token
    options['v'] = '5.80'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def getUserinfo():
    return call('users.get')

def wall():
    print('Работаем со стеной.')
    wall = call('wall.get')
    wall = wall['response']['items']
    for post in wall:
        call('wall.delete', post_id = post['id'])
        time.sleep(3)
        pprint('Удален пост со стены номер %s' % post['id'])

def docs():
    print('Работаем с документами')
    userid = getUserinfo()['response'][0]['id']
    docs = call('docs.get')
    docs = docs['response']['items']
    for doc in docs:
        call('docs.delete', doc_id = doc['id'], owner_id = userid)
        pprint('Удален документ номер %s' % doc['id'])
        time.sleep(3)

def groups():
    print('Работаем с группами')
    groups = call('groups.get')['response']['items']
    for group in groups:
        call('groups.leave', group_id = group)
        pprint('Удалена группа %s' % group)

def photos():
    print('Работаем с фотографиями')
    userid = getUserinfo()['response'][0]['id']
    getAlbums = call('photos.getAlbums', need_system = 1)['response']['items']
    print('Получили список альбомов.')
    for album in [a['id'] for a in getAlbums]:
        photos = call('photos.get', owner_id = userid, album_id = album)
        print('Выбрали альбом.')
        for photo in [p['id'] for p in photos['response']['items']]:
            call('photos.delete', photo_id = photo, owner_id = userid)
            pprint('Удалено фото %s' % photo)

def videos():
    #почему-то не работает. в будущем обновлении запилю.
    print('Работаем с видозаписями')
    userid = getUserinfo()['response'][0]['id']
    videoGet = call('video.get')['response']['items']
    for video in [v['id'] for v in videoGet]:
        call('video.delete', video_id = video, target_id = userid)
        print('Удалено видео %s' % video)

def messages():
    dialogs = []
    resp = call('messages.getDialogs', count=1)
    count = resp['response']['count']
    calls200 = int(count / 200)
    callsext = count % 200
    peer_id = lambda m: m['chat_id'] + 2000000000 if 'chat_id' in m else m['user_id']
    for i in range(calls200):
        resp = call('messages.getDialogs',
                       count=200,
                       offset=200 * i)
        dialogs += resp['response']['items']
    if callsext:
        resp = call('messages.getDialogs',
                       count=callsext,
                       offset=200 * calls200)
        dialogs += resp['response']['items']
    dialogs = [peer_id(m['message']) for m in dialogs]
    for dialog in dialogs:
        call('messages.deleteConversation', peer_id=dialog)
        print('Удалены сообщения от %s' % dialog)
        time.sleep(2)

token = input('Прощай, ВКонтакте. Введите ваш токен (его можно получить например здесь https://vkhost.github.io/): ')
while True:
    print('Прощай, ВКудахт!')
    option = input("""1) Удалить всё со стены
    2) Удалить всё в разделе документов
    3) Отписаться от всех пабликов
    4) Удалить все фотографии из всех альбомов
    5) Удалить все видео (почему-то не работает)
    6) Удалить все диалоги
    q) Выйти
    >>> """)
    if option == '1': wall()
    elif option == '2': docs()
    elif option == '3': groups()
    elif option == '4': photos()
    elif option == '5': videos()
    elif option == '6': messages()
    elif option == 'q': exit()
    else: print('[!] Неправильный ввод')
