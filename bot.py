from vk_api import *
from keyboards import Keyboard, data
import time as t
import json, random, os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk = VkApi(token="31ea1c0cbb198afcd96b368fee90eea2bc472e643c3923b20374b6886468ef0b8c00455ce0aa81f396447")
vk._auth_token()

options = json.loads(open("options.json", 'r').read())

asking_question = []
ignore = []

code = 0

def get_user(user_id):
	info = vk.method("users.get", {"user_ids": user_id})[0]
	return "{} {} vk.com/id{}\n".format(info['first_name'], info['last_name'], user_id)

def find(string, tags):
    """ Функция возвращающая True, если в string найдётся tag """
    ret = False
    for tag in tags:
        if string.lower().count(tag) != 0:
            ret = True
    return ret

def write_text(user_id, random_id, message):
	global vk
	vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message})

def send_keyboard(user_id, random_id, message, keyboard):
	global vk
	vk.method('messages.send', {'user_id': user_id, 'random_id': random_id, 'message': message, 'keyboard': keyboard})


def tell_moders(moder_id, message, user_id):
	global vk, options
	moder_info = vk.method("users.get", {"user_ids": moder_id})[0]
	user_info = vk.method("users.get", {"user_ids": user_id})[0]
	for moder in options['moderators']:
		if moder != moder_id:
			vk.method('messages.send', {'user_id': user_id, 'random_id': random.randint(10000, 1000000),
			 'message': "{} {} {} {} {} ({})".format(moder_info['first_name'],
			 	moder_info['last_name'], message, user_info['first_name'],
			 	 user_info['last_name'], user_id)})

def call_moderators(user_id):
	global vk, options
	info = vk.method("users.get", {"user_ids": user_id})[0]
	for moder in options['moderators']:
		keyboard = VkKeyboard(inline=True)
		keyboard.add_button("Откликнуться {}".format(user_id), color=VkKeyboardColor.POSITIVE)
		keyboard.add_line()
		keyboard.add_button("Завершить {}".format(user_id), color=VkKeyboardColor.NEGATIVE)
		keyboard.add_line()
		keyboard.add_button("Отменить {}".format(user_id), color=VkKeyboardColor.DEFAULT)
		send_keyboard(moder, random.randint(10000, 1000000), 
			"Новый вопрос у пользователя {} {}".format(info['first_name'], info['last_name']), keyboard.get_keyboard())



sorry = '\n\nЕсли вы не получили нужного ответа, то нажмите напишите "Связаться с консультантом". Уверен они Вам точно помогут'

while True:
	requests = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unread"})
	for request in requests['items']:
		user_id = request['last_message']['from_id']
		text = request['last_message']['text']
		random_id = request['last_message']['random_id']

		if text == "/moders":
			answer = "Список модераторов:\n"
			for moder in options['moderators']:
				answer += get_user(moder)
			write_text(user_id, random_id, answer)
			continue

		if user_id in options['moderators']:
			if text.count("Откликнуться") > 0:
				tell_moders(user_id, "откликнулся на запрос", int(text[13:]))
				vk.method('messages.markAsRead', {'peer_id': user_id})
				continue
			if text.count("Завершить") > 0:
				customer_id = int(text[9:])
				if customer_id in ignore:
					ignore.remove(customer_id)
					tell_moders(user_id, "завершил разговр с клиентом", int(text[9:]))
				else:
					write_text(user_id, random.randint(10000, 100000) , "Ошибка. Сианс с {} уже был завершён".format(customer_id))
				vk.method('messages.markAsRead', {'peer_id': user_id})
				continue
			if text.count("Отменить") > 0:
				customer_id = int(text[8:])
				if customer_id not in ignore:
					ignore.append(customer_id)
					tell_moders(user_id, "отменил действие по завершению разговора с клиентом", customer_id)
				else:
					write_text(user_id, random.randint(10000, 100000), "Ошибка. Сианс с {} уже идёт".format(customer_id))

		if user_id in ignore:
			continue

		if user_id in asking_question:
			ok = False

			for question in data['questions']:
				if find(text, question['tags']):
					send_keyboard(user_id, random_id, question['answer'] + sorry, Keyboard['FAQ'])
					ok = True
					break

			if text == "Связаться с консультантом":
				ignore.append(user_id)
				asking_question.remove(user_id)
				call_moderators(user_id)
				write_text(user_id, random_id, "Ваш вопрос был передан консультанту и уже обробатывается. Подождите немного")
				continue

			if not ok:
				write_text(user_id, random_id, "Ваш вопрос был передан консультанту и уже обробатывается. Подождите немного")
				call_moderators(user_id)
				ignore.append(user_id)
				asking_question.remove(user_id)
				continue

		if text == "Начать":
			send_keyboard(user_id, random_id, data['speach']['start']['text'], Keyboard['start'])
			continue

		if text == data['speach']['getting_order']['button_text']:
			send_keyboard(user_id, random_id, data['speach']['getting_order']['text'], Keyboard['order1'])
			continue

		if (text == data['speach']['choosed_color']['button_text1'] or 
			text == data['speach']['choosed_color']['button_text2']):
			write_text(user_id, random_id, data['speach']['choosed_color']['text'])
			continue

		if text == data['speach']['other_color']['button_text']:
			write_text(user_id, random_id, data['speach']['other_color']['text'])
			continue

		if text == data['speach']['asking_question']['button_text']:
			write_text(user_id, random_id, data['speach']['asking_question']['text'])
			asking_question.append(user_id)
			continue

		if text == "Назад":
			send_keyboard(user_id, random_id, "", start)
			continue




	t.sleep(1)
