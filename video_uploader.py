'''Данный скрипт ищет видео с расширением .webm и перекодирует их в .mp4 при помощи ffmpeg и постит это видео в группу. 
Также, данный скрипт постит все видео с разрешением mp4 и удаляет их из каталога.
Тестировано на Ubuntu 18.04'''

import time, os, requests

def convert(file):
    '''Конвертирует файл при помощи ffmpeg в mp4'''
    newfile = str(int(time.time() * 1000)) + '.mp4'
    command = 'ffmpeg -i %s %s' % (repr(file), repr(newfile))
    print('executing: %s'%command)
    errorlevel = os.system(command)
    print('ffmpeg: %s'%('ok' if not errorlevel else 'failed'))
    if not errorlevel:
    	os.remove(file)
    return newfile, errorlevel

def upload_video(file):
    '''Загружает файл в сообщество ВКонтакте и удаляет его локальную копию.'''
    data = {
        'video_file': open(file, 'rb')
    }
    group = 'id группы'
    token = 'Токен группы'
    name = 'Название видео'
    description =  'Описание'
    resp = requests.get('https://api.vk.com/method/video.save?group_id={group}&name={name}&description={description}&access_token={token}&v=5.80'.format(group = group, token=token, name=name, description=description)).json()
    upload_server = resp['response']['upload_url']
    uploading = requests.post(upload_server, files = data).json()
    print(uploading)
    print(file)
    os.remove(file)

print('Starting script.')

for fname in os.listdir('.'):
    name, ext = os.path.splitext(fname)
    if ext == '.webm':
        new_name, errorlevel = convert(fname)
        if not errorlevel:
            upload_video(new_name)
    elif ext == '.mp4':
        upload_video(fname)
    else:
        print('Invalid file type: *%s (%s)'%(ext, fname))
