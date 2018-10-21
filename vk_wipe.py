# coding = utf-8
'''Вайпалка, дорогие диванные воены. '''
import requests
import random
import time
import string

def call(method, options={}, **kwargs):
    options['access_token'] = access_token
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def send_message(peer_id, textmessage='',photovar=''):
    options = {
        'message' : textmessage,
        'peer_id' : peer_id,
    }
    if photovar != '':
        options['attachment'] = 'photo' + photovar
    call('messages.send', options)
    print('Отправлено {textmessage} и {photovar} в {peer_id}'.format(textmessage = textmessage, photovar = photovar, peer_id = peer_id))

def stringGen(length):
	textmessage = ''
	for _ in range(int(length)):
		textmessage += random.choice(string.printable)
	return textmessage

def wipe_text(messagecount, peer_id, timer, textmode, length=1, textmessage='sometext'):
	if textmode == '1':
	    for _ in range(messagecount):
	        try:
	            time.sleep(timer)
	            send_message(peer_id, textmessage)
	        except Exception as e:
	            print(e)
	elif textmode == '2':
		for _ in range(messagecount):
			try:
				textmessage = stringGen(length)
				time.sleep(timer)
				send_message(peer_id, textmessage)
			except Exception as e:
				print(e)

def wipe_pictures(messagecount, peer_id, timer, photomode, photo='<owner_id>_<media_id>', album='saved'):
    if photomode == '1':
        for _ in range(messagecount):
            try:
                time.sleep(timer)
                send_message(peer_id, '', photo)
            except Exception as e:
                print(e)
    elif photomode == '2':
        for _ in range(messagecount):
            try:
                time.sleep(timer)
                photos = call('photos.get', album_id=album)['response']['items']
                random.shuffle(photos)
                send_message(peer_id, '', '{owner_id}_{id}'.format(**random.choice(photos)))
            except Exception as e:
                print(e)

def main():
    print('Вайпалка от Kiriharu!')
    option = input('''Выбери свой путь:
    1) Вайп текстом (рандомным и выбранным)
    2) Вайп картинками (из сохранённого альбома и конкретной пикчей)
    >>>''')
    messagecount = input('Введите количество сообщений для вайпа: ')
    peer_id = input('Введите ID чата: ')
    timer = input('Введите время между постингом: ')
    if option == '1':
    	textmode = input('Введите режим работы. 1 - спам конкретного сообщения, 2 - спам рандомными сообщениями: ')
    	if textmode == '1':
    		textmessage = input('Введите текст для вайпа: ')
    		wipe_text(int(messagecount), peer_id, int(timer), textmode, textmessage = textmessage)
    	elif textmode == '2':
    		length = input('Введите размер генерируемого текста: ')
    		wipe_text(int(messagecount), peer_id, int(timer), textmode, length = length)
    elif option == '2':
    	photomode = input('Введите режим работы. 1 - спам выбранной картинкой, 2 - спам с выбранного альбома.')
    	if photomode == '1':
    		photo = input('Введите имя фото в виде <owner_id>_<media_id>: ')
    		wipe_pictures(int(messagecount), peer_id, int(timer), photomode, photo = photo)
    	elif photomode == '2':
    		album = input('Введите название или id альбома. Например, saved: ')
    		wipe_pictures(int(messagecount), peer_id, int(timer), photomode, album = album)


if __name__ == '__main__':
	access_token = input('Введите access token: ')
	main()
	