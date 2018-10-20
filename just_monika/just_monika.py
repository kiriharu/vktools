# coding = utf-8

'''Данный скрипт постит сообщения из dialog.txt и фото (если указано) в выбранный диалог. За пример диалога взяты реплики из игры Doki Doki Literature Club в сцене с Моникой.'''
import requests, time

id = input('Введите ID диалога: ')
timer = input('Введите задержку при постинге в секундах (минимальная задержка 5 секунд): ')
photo = input('Введите фото в виде <owner_id>_<media_id>: ')

def call(method, options={}, **kwargs):
    '''Фукнция вызова api ВК.'''
    options['access_token'] ='Сюда вводить токен'
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp
def send_message(id, textmessage='',photovar=''):
    '''Функция отправки сообщений.'''
    options = {
        'message' : textmessage,
        'peer_id' : id,
    }
    if photovar != '':
        options['attachment'] = 'photo' + photovar
    call('messages.send', options)
    print('Отправлен {message} и {photo} к {id}'.format(message = textmessage, photo = photovar, id = id))
def main(id, timer, photo):
    '''Just Monika. Пишет сообщения из файла dialog.txt выбранному id отправляя фото photo, раз в timer секунд
    id - номер диалога,
    photo - постит фото, если фото не указано(пустой аргумен, постит без него),
    timer - задержка при постинге в секундах.'''
    file = open('dialog.txt', encoding='utf-8', newline='')
    timer = int(timer)
    while True:
        for line in file:
            time.sleep(timer)
            send_message(id, line, photo)


if __name__ == '__main__':
    main(id, timer, photo)