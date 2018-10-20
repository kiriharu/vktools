# coding = utf-8
'''Данный скрипт побуквенно изменяет сообщение. Получается что-то вроде ввода сообщения по буквам (я не знаю как это объяснить, просто попробуйте ;c)'''
import requests, time
def call(method, options={}, **kwargs):
    '''Фукнция вызова api ВК.'''
    options['access_token'] ='Сюда токен'
    options['v'] = '5.73'
    options.update(kwargs)
    resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
    if 'error' in resp:
        print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
    return resp

def send_message(id, message):
    '''Функция отправки сообщений.'''
    options = {
        'message' : message,
        'peer_id' : id,
    }
    message_id = call('messages.send', options)['response']
    print('Message {0} sended'.format(message))
    print(message_id)
    return message_id

def main():
    '''Изменяет сообщение побуквенно и выводит его
    id - id беседы
    message - любое сообщение'''
    id = input("Enter id: ")
    message = input("Enter message: ")
    lastmessage = message[0]
    message_id = send_message(id, lastmessage)
    for i in message[1:]:
        lastmessage += i
        options = {
            'peer_id': id,
            'message': lastmessage,
            'message_id': message_id
        }
        print(i)
        time.sleep(1)
        call('messages.edit', options)

if __name__ == '__main__':
    main()