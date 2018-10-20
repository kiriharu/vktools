import requests

VERSION = 3
DEBUG = False

class VK(object):
    """docstring for VKBot"""
    def __init__(self, access_token=None, api_url='https://api.vk.com/method/{method}'):
        self.access_token = access_token
        self.api_url = api_url
        self.longpoll_data = None
        self.api_version = '5.78'
    def auth(self, login, password):
        args = {}
        args['username'] = login
        args['password'] = password
        args['v'] = self.api_version
        args['grant_type'] = 'password'
        args['client_id']  = '3697615'
        args['client_secret'] = 'AlVXZFMUqyrnABp8ncuU'
        try:
            r = requests.get('https://oauth.vk.com/token', params=args).json()
        except Exception as e:
            return False, e
        if 'access_token' in r:
            self.access_token = r['access_token']
            return True, self.access_token
        return False, r
    def call(self, method, dictargs=None, **kwargs):
        if not dictargs:
            dictargs = {}
        dictargs.update(kwargs)
        if self.access_token not in ['anonymous', None]:
            dictargs['access_token'] = self.access_token
        dictargs['v'] = self.api_version
        url = self.api_url.format(method=method)
        req = requests.get(url, params=dictargs)
        response = req.json()
        if DEBUG:
            print('GET <', req.url)
            print('GET >', req.text)
        if 'response' in response:
            return True, response['response']
        else:
            err_resp = self.on_error(response['error']['error_code'], response['error']['error_msg'], response['error'])
            if err_resp:
                dictargs.update(err_resp)
                return self.call(method, dictargs)
            if response['error']['error_code'] == 14: # captcha
                captcha_data = response['error']
                captcha_sid = captcha_data['captcha_sid']
                captcha_img = captcha_data['captcha_img']
                captcha = self.on_captcha(captcha_img, captcha_sid)
                if captcha:
                    dictargs.update({
                            'captcha_sid': captcha_sid,
                            'captcha_key': captcha
                        })
                    return self.call(method, dictargs)
            return False, response['error']
    def post(self, url, **kwargs):
        req = requests.post(url, **kwargs)
        if DEBUG:
            print('POST <', req.url)
            print('POST >', req.text)
        response = req.json()
        if 'error' in response:
            return False, response
        else:
            return True, response

    def check_auth(self):
        succ, response = self.call('users.get', fields='domain')
        if not succ:
            return False, None
        if len(response) == 0:
            return False, None
        return True, response[0]
    def get_longpoll_server(self):
        if self.lp_mode == 0:
            succ, data = self.call('messages.getLongPollServer', lp_version=2)
        else:
            succ, data = self.call('groups.getLongPollServer', lp_version=2, group_id=self.lp_mode)
        return 'key' in data and succ, data
    def update_longpoll_server(self, mode=0):
        '''
        Long Polling modes:
            0 - user
            group_id - group
        '''
        self.lp_mode = mode
        succ, data = self.get_longpoll_server()
        if not succ:
            return False, data
        self.on_longpoll_update(succ, data)
        self.longpoll_data = data
        return True, data
    def longpoll_get(self):
        if not self.longpoll_data:
            self.update_longpoll_server()
        url = 'https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=255&version=3'.format(**self.longpoll_data)
        data = requests.get(url).json()
        if 'failed' in data:
            fcode = data['failed']
            self.on_longpoll_error(fcode, data)
            if fcode == 1:
                self.longpoll_data['ts'] = data['ts']
                return self.longpoll_get()
            elif fcode == 2:
                self.update_longpoll_server()
                return self.longpoll_get()
            elif fcode == 3:
                return []
            elif fcode == 4:
                return []
        self.on_longpoll_event(data)
        self.longpoll_data['ts'] = data['ts']
        return data['updates']
    def on_longpoll_error(self, error_code, data):
        pass
    def on_longpoll_event(self, data):
        pass
    def on_longpoll_update(self, success, data):
        pass
    def on_error(self, error_code, error_msg, args):
        pass
    def on_captcha(self, captcha_img, captcha_sid):
        return None
    def send_message(self, peer_id, **kwargs):
        message = kwargs.get('message', '')
        attachments = [str(v) for v in kwargs.get('attachments', [])]
        forwarded = [str(v) for v in kwargs.get('fwd_messages', [])]
        succ, response = self.call('messages.send',
            peer_id=peer_id,
            message=message,
            attachment=','.join(attachments),
            fwd_messages=forwarded)
        if succ:
            return True, response
        return False, response
    def send_voice(self, peer_id, path, **kwargs):
        if type(path) == str:
            file = open(path, 'rb')
        elif type(path) == bytes:
            file = (path, 'audio_message.ogg')
        else:
            return False, 'invalid variable type for path_or_data'
        succ, server = self.call('docs.getMessagesUploadServer', type='audio_message')
        if not succ:
            return False, server
        succ, doc = self.post(server['upload_url'], files=dict(
            file=file
        ))
        if not succ:
            return False, doc
        succ, document = self.call('docs.save', file=doc['file'],
            title='audio_message.ogg')
        if not succ:
            return False, document
        succ, resp = self.send_message(peer_id, **kwargs,
            attachments=['doc{owner_id}_{id}'.format(**document[0])])
        return succ, resp
    def upload_photo(self, path_or_data):
        if type(path_or_data) == str:
            file = open(path_or_data, 'rb')
        elif type(path_or_data) == bytes:
            file = (path_or_data, 'photo')
        else:
            return False, 'invalid variable type for path_or_data'
        succ, server = self.call('photos.getMessagesUploadServer', type='audio_message')
        if not succ:
            return False, server
        succ, pho = self.post(server['upload_url'], files=dict(
            photo=file
        ))
        if not succ:
            return False, pho
        succ, photo = self.call('photos.saveMessagesPhoto', **pho)
        if not succ:
            return False, photo
        return True, 'photo{owner_id}_{id}'.format(**photo[0])
    def send_photo(self, peer_id, paths, **kwargs):
        photos = []
        if not isinstance(paths, list):
            paths = [paths]
        for p in paths:
            s, r = self.upload_photo(p)
            if s:
                photos.append(r)
            else:
                return False, r
        if DEBUG:
            print('PHOTOS:', photos)
        succ, resp = self.send_message(peer_id, **kwargs,
            attachments=photos)
        return succ, resp
        
class longpoll_codes:
    def __init__(self):
        self.flag_modify = 1
        self.flag_set = 2
        self.flag_reset = 3
        self.new_message = 4
        self.edit_message = 5
        self.read_all_input = 6
        self.read_all_output = 7
        self.friend_now_online = 8
        self.friend_now_offline = 9
        self.flag_dialog_reset = 10
        self.flag_dialog_edit = 11
        self.flag_dialog_set = 12
        self.messages_delete_all = 13
        self.messages_revieve = 14
        self.chat_edited = 51
        self.user_typing = 61
        self.chat_typing = 62
        self.counter_changed = 80
        self.notify_changed = 114
    def get_name(self, code):
        keys = {}
        for k in dir(self):
            if type(self.__getattribute__(k)) == int:
                keys[k] = self.__getattribute__(k)
        for k, v in keys.items():
            if v == code:
                return k
        return code
class longpoll_messages_flags:
    def __init__(self):
        self.unread = 1 
        self.outbox = 2 
        self.replied = 4 
        self.importnant = 8 
        self.chat = 16 
        self.friends = 32 
        self.spam = 64 
        self.deleted = 128 
        self.fixed = 256 
        self.media = 512 
        self.hidden = 65536 
        self.delete_for_all = 131072 
    def get_name(self, code):
        keys = {}
        for k in dir(self):
            if type(self.__getattribute__(k)) == int:
                keys[k] = self.__getattribute__(k)
        for k, v in keys.items():
            if v == code:
                return k
        return code
    def get_flags(self, codes_sum):
        bits = []
        for v in range(18):
            if codes_sum & (2 ** v):
                bits.append(2 ** v)
        flags = []
        for bit in bits:
            flags.append(self.get_name(bit))
        return flags
class VKLongpollCodes(object):
    """docstring for VKLongpollCodes"""
    def __init__(self):
        super(VKLongpollCodes).__init__()
        self.messages = longpoll_messages_flags()
        self.codes = longpoll_codes()
VKLongpollCodes = VKLongpollCodes()
del longpoll_messages_flags
del longpoll_codes

devices = [
    'none',
    'Phone',
    'Iphone',
    'IPad',
    'Android',
    'Windows Phone',
    'Windows',
    'Web'
]
logout_codes = [
    'logout',
    'timeout'
]




def check_updates():
    print('[gitdl] Checking for updates...', end='', flush=True)
    try:
        data = requests.get('https://raw.githubusercontent.com/undefinedvalue0103/pylibs/master/versions.json').json()
    except:
        print('failed')
        return False
    print('done')
    api_data = data.get('vkapi')
    if not api_data:
        print('[gitdl] Library info is unavailable')
        return False
    if api_data['version_num'] > VERSION:
        print('[gitdl] Updates available')
        return True
    print('[gitdl] Latest version installed')
    return False
def install_update(force=False):
    if force or check_updates():
        print('[gitdl] Loading...', end='', flush=True)
        try:
            data = requests.get('https://raw.githubusercontent.com/undefinedvalue0103/pylibs/master/vkapi.py').content
        except:
            print('failed')
            return False
        print('done')
        print('[gitdl] Saving...', end='', flush=True)
        with open('vkapi.py', 'wb') as f:
            f.write(data)
        print('done')
        return True
    return False