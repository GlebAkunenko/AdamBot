from vk_api import *
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

data = json.loads(open("data.txt", 'r', encoding='utf-8').read())

Keyboard = dict()

keyboard = VkKeyboard(one_time=True)
keyboard.add_button(data['speach']['getting_order']['button_text'], color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button(data['speach']['asking_question']['button_text'], color=VkKeyboardColor.PRIMARY)
keyboard.add_button(data['speach']['reviews']['button_text'], color=VkKeyboardColor.DEFAULT)
Keyboard['start'] = keyboard.get_keyboard()

keyboard = VkKeyboard(one_time=False)
keyboard.add_button(data['speach']['choosed_color']['button_text1'], color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button(data['speach']['choosed_color']['button_text2'], color=VkKeyboardColor.DEFAULT)
keyboard.add_line()
keyboard.add_button(data['speach']['other_color']['button_text'], color=VkKeyboardColor.NEGATIVE)
Keyboard['order1'] = keyboard.get_keyboard()

keyboard = VkKeyboard(inline=True)
keyboard.add_button("Связаться с консультантом", color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button(data['speach']['getting_order']['button_text'], color=VkKeyboardColor.POSITIVE)
keyboard.add_button("Назад", color=VkKeyboardColor.NEGATIVE)
Keyboard['FAQ'] = keyboard.get_keyboard()