import requests, json, random
#https://pastebin.com/3pBQk4rh - pasts for this script, if you need
TOKEN = ''
messages = {} #for default.
def call(method, options={}, **kwargs):
	'''Call method with some options. Kwargs for other items.'''
	options['access_token'] = TOKEN
	options['v'] = '5.73'
	options.update(kwargs)
	resp = requests.get('https://api.vk.com/method/'+method, params=options).json()
	if 'error' in resp:
	    print('VKERROR: {error_code}: {error_msg}'.format(**resp['error']))
	return resp

def send_message(message, peer_id):
	'''Send message function. Message sending to peer_id'''
	options = { 'peer_id' : peer_id, 'message' : message }
	return call('messages.send', options=options)

def jsonsave():
	'''Save or create json file messages.json'''
	with open('messages.json', 'w', encoding='utf8') as f:
		f.write(json.dumps(messages, ensure_ascii=False, indent=4))

def jsonload():
	'''Loading json file. If file dont exist - call jsonsave()'''
	global messages
	try:
		messages = json.loads(open('messages.json', 'r', encoding='utf8').read())
	except:
		print('Database created, pls add new messages to send')
		jsonsave()

def message_add(message):
	'''Function to add messages to messages.json


	If message added without exceptions - function return True. If exception has occured = return False
	Function accept message string.'''
	try:
		messages[message] = {}
		jsonsave()
		return True
	except:
		return False

def getkey():
	'''Return random message from messages.json (from messages)'''
	return (random.choice(list(messages.items())))

def main():
	'''Some main loop.'''
	#get data from messages.getLongPollServer
	data = requests.get('https://api.vk.com/method/messages.getLongPollServer',
	                    params={'access_token': TOKEN, 'v' : '5.73'}).json()['response']
	#starting longpoll loop
	while True:
	    response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(
	    server=data['server'], 
	    key=data['key'], 
	    ts=data['ts'])).json()
	    try:
	    	updates = response['updates']
	    except KeyError:
	    	#if KeyError occured - get new data from messages.getLongPollServer.
	    	data = requests.get('https://api.vk.com/method/messages.getLongPollServer',params={'access_token': TOKEN, 'v' : '5.73'}).json()['response']	
	    	continue
	    if updates:  
	        for element in updates: 
	            action_code = element[0] 
	            if action_code == 4:
	            	poster = element[6]['from']
	            	from_id = element[3]
	            	if from_id == peer_id:
	            		#if poster not script user - go
	            		if poster != admin:
	            			#getting random message
			            	message = getkey()
			            	#posting!
			            	send_message(message, peer_id)
			            	#and debug с:
			            	print('sended %s to %s' % (message, peer_id))
	    data['ts'] = response['ts']

if __name__ == '__main__':
	TOKEN = input('Enter you VK access_token: ')
	admin = str(call('users.get')['response'][0]['id']) # get script user id
	jsonload() # loading json database
	#menu. Just menu.
	option = input('Welcome to troll bot. type edit for edit, any key to start: ')
	if option == 'edit':
		text = ''
		while text != 'exit':
			text = input('Enter some text. Enter exit for exit: ')
			if text != 'exit':
				output =message_add(text)
				if output == True:
					print('Success! ')
				else: print('Lol, exception has occured.')
	else:
		peer_id = int(input('Enter peer_id: '))
		main()