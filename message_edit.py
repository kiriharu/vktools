# coding = utf-8
'''Данный скрипт побуквенно изменяет сообщение. Получается что-то вроде ввода сообщения по буквам (я не знаю как это объяснить, просто попробуйте ;c)'''
import requests, time
def call(method, options={}, **kwargs):
    '''Фукнция вызова api ВК.'''
    options['access_token'] = token 
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def send_message(peer_id, message):
    '''Функция отправки сообщений.'''
    options = {
        'message' : message,
        'peer_id' : peer_id,
    }
    message_id = call('messages.send', options)['response']
    print('Сообщение {} отправлено'.format(message))
    print('Работаем с сообщением с ID {}'.format(message_id))
    return message_id

def main(peer_id, message):
    '''Изменяет сообщение побуквенно и выводит его
    peer_id - id беседы
    message - любое сообщение'''
    lastmessage = message[0]
    message_id = send_message(peer_id, lastmessage)
    for i in message[1:]:
        lastmessage += i
        options = {
            'peer_id': peer_id,
            'message': lastmessage,
            'message_id': message_id
        }
        print('Добавлена буква {}'.format(i))
        time.sleep(1)
        call('messages.edit', options)

if __name__ == '__main__':
    token = input("Введите токен: ")
    peer_id = input("Введите ID чата: ")
    message = input("Введите сообщение: ")
    main(peer_id, message)