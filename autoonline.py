'''Данный скрипт позволяет устанавливать автоонлаин, автостатус и автоматическое добавление в друзья нескольким аккаунтам.
Принцип работы прост - сначала выполяется установка онлаина на первый аккаунт, потом добавление в друзья, установка статуса. 
Дальше идёт следующий аккаунт и так далее.

Требует vkapi от Undefined Value - https://github.com/undefinedvalue0103/pylibs/blob/master/vkapi.py'''
import vkapi, time
start_t = time.time()
classes = []
tokens = ['Сюда вводить токены', 'а вот это второй токен.']
for token in tokens:
    classes.append(vkapi.VK(token))

while True:
    for i, api in enumerate(classes):
        # Ставим онлайн
        success, resp = api.call('account.setOnline', {})
        if success:
            print("Аккаунт #%s онлайн" % (i + 1))
        else:
            print("Что-то не так с аккаунтом #{acc}. Проверьте скрипт. (account.setOnline error)".format(acc=i+1))
        time.sleep(10)
        #Добавляем в друзья
        success, resp = api.call('friends.getRequests', {})
        if success:
            for uid in resp['items']:
                r = api.call('friends.add', {'user_id': uid})
                print("Аккаунт #{acc} добавил в друзья {uid}".format(acc=i+1, uid=uid))
        else:
            print("Что-то не так с аккаунтом #{acc}. Проверьте скрипт. (friends.getRequests error)".format(acc=i+1))
        time.sleep(10)
        #Считаем часы. Прошу, не бейте :c
        upt = int(time.time() - start_t)
        seconds = str(upt % 60).zfill(2)
        upt = int(upt / 60)
        minutes = str(upt % 60).zfill(2)
        hours = str(int(upt / 60)).zfill(2)
        upt_s = hours + ':' + minutes + ':' + seconds
        server_time = time.strftime('%H:%M:%S')
        text = 'Время сервера: ' + server_time +  '| Автоприём заявок в друзья | Время работы: ' + str(upt_s)
        #ставим MOTD
        success, resp = api.call('status.set', {'text': text})
        if success:
            print("Уставновлено MOTD для аккаунта #%s" % (i + 1))
        else:
            print("Что-то не так с аккаунтом #{acc}. Проверьте скрипт. (status.set error)".format(acc=i+1))