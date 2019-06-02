import requests
import random
import time

TOKEN = 'ENTER TOKEN HERE'


class VK:
    def __init__(self, token, v='5.95'):
        self.token = token
        self.v = v

    def call(self, method, options={}, **kwargs):
        options['access_token'] = TOKEN
        options['v'] = '5.95'
        options.update(kwargs)
        resp = requests.get('https://api.vk.com/method/' + method, params=options).json()
        return resp

    def send_message(self, message, peer_id, attachment=None):
        options = {
            "peer_id": peer_id,
            "message": message,
            "random_id": random.randint(100, 999)
        }

        if attachment:
            options['attachment'] = attachment

        return self.call('messages.send', options=options)

    def get_conversations_by_id(self, peer_ids):
        options = {
            "peer_ids": peer_ids,
        }
        return self.call("messages.getConversationsById", options=options)

    @staticmethod
    def chunks(l, n):
        """
        Yield successive n-sized chunks from l.

        https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        """
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def get_valid_confs(self, startid, maxid):

        valid = []
        invalid = []

        confslist = [i+2000000000 for i in range(startid, maxid)]
        for conflist in VK.chunks(confslist, 100):
            confs = ', '.join(map(str, conflist))
            try:
                confresp = self.get_conversations_by_id(confs)['response']['items']
                for conf in confresp:
                    if conf['can_write']['allowed'] is True:
                        valid.append(conf['peer']['id'])
                    else:
                        invalid.append(conf['peer']['id'])
            except Exception as e:
                print(f"Exception occured:  {e}")
        print(f"DEBUG: Valid: {len(valid)}, Invalid: {len(invalid)}")
        return valid, invalid

    def masssender(self, ids, message, timer, attachment=None):
        i = 0
        for confid in ids:
            resp = self.send_message(message, confid, attachment)
            while 'error' in resp:
                if resp['error']['error_code'] == 14:
                    print("Founded captcha! Waiting 10-30 sec.")
                    print(f"DEBUG: {resp}")
                    sleeping = random.randint(10, 30)
                    print(f"Waiting {sleeping}")
                    time.sleep(sleeping)
                if resp['error']:
                    print(f"Another error has occured: {resp}")
            print(f"Sended {message} to {confid} (message id: {resp['response']})")
            time.sleep(int(timer))
            i = i + 1
        return i


if __name__ == '__main__':
    vk = VK(token=TOKEN)
    print(f"Loaded token {TOKEN}\n")

    is_id_valid = True
    minid = 0
    maxid = 0

    while is_id_valid:
        minid = input("Enter minid for confs (Enter like 1 or 100): ")
        maxid = input("Enter maxid for confs (Enter like 1 or 100): ")
        if int(minid) > int(maxid):
            print("minid > maxid, type maxid < minid (like minid = 100, maxid = 200) + \n ")
        else:
            is_id_valid = False

    active, unactive = vk.get_valid_confs(int(minid), int(maxid))
    print(f"Active confs {active}")
    print(f"Unactive confs {unactive}")

    timer = input("Enter timer to send messages (in sec): ")
    message = input("Print message to massend: ")
    attachment = input("Print attachment like <type><owner_id>_<media_id> (if u don't need attachment - press enter): ")

    confirm = input(f"""
Message = {message}
Activeconfs = {active}
Attachment = {attachment}
Are you sure? Type y or n
    """)

    while True:
        if confirm.lower() == 'y':
            result = vk.masssender(active, message, timer, attachment)
            exit(f"Done! Sended {result} messages.")
        if confirm.lower() == 'n':
            exit("Exited.")
        print("Type y or n.")

