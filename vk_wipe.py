# coding = utf-8
'''Вайпалка, дорогие диванные воены. Ваш опонент не прав и не хочет слушать вас? Пускай выслушает стену текста!
Есть 5 режима вайпа: вайп обычным текстом, вайп картинкой, вайп картинкой и текстом, вайп рандомным текстом и картинкой, вайп рандомным текстом.
В случае рандомного текста - он конкатенируется с предыдущим.'''
import requests
import random
from datetime import time
import time

access_token = input("Enter access_token: ")

def call(method, options={}, **kwargs):
    global access_token
    options['access_token'] = access_token
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def send_message(id, textmessage='',photovar=''):
    options = {
        'message' : textmessage,
        'peer_id' : id,
    }
    if photovar != '':
        options['attachment'] = 'photo' + photovar
    call('messages.send', options)
    print('Message' + '(' + textmessage + ')' + 'and photo' + photovar + 'send to' + '(' + id + ')' )
    return

def wipe_text(messagecount, id, timer):
    textmessage = input("Enter message to send(if nothing entered message text is wipe): ")
    i = 0
    while i < int(messagecount):
        try:
            time.sleep(int(timer))
            send_message(id, textmessage)
            i = i + 1
        except Exception as e:
            print(e)
def wipe_pictures(messagecount, id, timer):
    photomode = input("Enter photomode: \n 1) Post choosed photo \n 2) Post random photo \n")
    if photomode == '1':
        photo = input("Enter id photo in <owner_id>_<media_id> type: ")
        i = 0
        while i < int(messagecount):
            try:
                time.sleep(int(timer))
                send_message(id, '', photo)
                i = i + 1
            except Exception as e:
                print(e)
    if photomode == '2':
        i = 0
        while i < int(messagecount):
            try:
                time.sleep(int(timer))
                photos = call('photos.get', album_id='saved')['response']['items']
                random.shuffle(photos)
                send_message(id, '', '{owner_id}_{id}'.format(**random.choice(photos)))
                i = i + 1
            except Exception as e:
                print(e)
def wipe_picturestext(messagecount, id, timer):
    photo = input("Enter id photo in <owner_id>_<media_id> type: ")
    textmessage = input("Enter message to send(if nothing entered message text is wipe): ")
    i = 0
    while i < int(messagecount):
        try:
            time.sleep(int(timer))
            send_message(id, textmessage, photo)
            i = i + 1
        except Exception as e:
            print(e)

def wipe_picturesrandomtext(messagecount, id, timer):
    photo = input("Enter id photo in <owner_id>_<media_id> type: ")
    chars = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&amp;*()")
    length = input("Input message length")
    textmessage = ''
    i = 0
    while i < int(messagecount):
        try:
            for _ in range(int(length)):
                textmessage += random.choice(chars)
            time.sleep(int(timer))
            send_message(id, textmessage, photo)
            i = i + 1
        except Exception as e:
            print(e)

def wipe_randomtext(messagecount, id, timer):
    chars = list("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!@#$%^&amp;*()")
    length = input("Input message length")
    i = 0
    textmessage = ''
    while i < int(messagecount):
        try:
            for _ in range(int(length)):
                textmessage += random.choice(chars)
            time.sleep(int(timer))
            send_message(id, textmessage)
            i = i + 1
        except Exception as e:
            print(e)

def main():
    print('Welcome to WIPE MACHINE by Kiriharu! All fucking rights recived')
    messagecount = input("Enter count of messages to post: ")
    id = input("Enter chat id: ")
    timer = input("Enter timer in seconds: ")
    option = input("Choose you way: \n 1) Text wipe \n 2) Picture wipe(included random mode) \n 3) Text and picture wipe \n 4) Random text and picture wipe \n 5) Random text wipe \n")
    if option == '1':
        wipe_text(messagecount,id,timer)
        main()
    elif option == '2':
        wipe_pictures(messagecount,id,timer)
        main()
    elif option == '3':
        wipe_picturestext(messagecount, id, timer)
        main()
    elif option == '4':
        wipe_picturesrandomtext(messagecount, id, timer)
        main()
    elif option == '5':
        wipe_randomtext(messagecount, id, timer)
        main()
    return

