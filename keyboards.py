from telebot import types
import json_functions as jf

data = jf.download_data()

clicker = types.KeyboardButton('/click!')
clicker_keyboard = types.ReplyKeyboardMarkup().add(clicker)


auto_upgrade_keyboard = types.InlineKeyboardMarkup()

auto_upgrade_calculator = types.InlineKeyboardButton(f'calculator', callback_data='calculator')
auto_upgrade_keyboard.add(auto_upgrade_calculator)

auto_upgrade_video_card = types.InlineKeyboardButton(f'video card', callback_data='video card')
auto_upgrade_keyboard.add(auto_upgrade_video_card)

auto_upgrade_pc = types.InlineKeyboardButton(f'pc', callback_data='pc')
auto_upgrade_keyboard.add(auto_upgrade_pc)

auto_upgrade_video_card_stand = types.InlineKeyboardButton(f'video card stand', callback_data='video card stand')
auto_upgrade_keyboard.add(auto_upgrade_video_card_stand)

auto_upgrade_quantum_computer = types.InlineKeyboardButton(f'quantum computer', callback_data='quantum computer')
auto_upgrade_keyboard.add(auto_upgrade_quantum_computer)

auto_upgrade_data_center = types.InlineKeyboardButton(f'data center', callback_data='data center')
auto_upgrade_keyboard.add(auto_upgrade_data_center)


clicker_upgrade_keyboard = types.InlineKeyboardMarkup()

clicker_upgrade_new_mouse = types.InlineKeyboardButton(f'new mouse', callback_data='new mouse')
clicker_upgrade_keyboard.add(clicker_upgrade_new_mouse)

clicker_upgrade_new_keyboard = types.InlineKeyboardButton(f'new keyboard', callback_data='new keyboard')
clicker_upgrade_keyboard.add(clicker_upgrade_new_keyboard)

clicker_upgrade_mechanical_keyboard = types.InlineKeyboardButton(f'mechanical keyboard', callback_data='mechanical '
                                                                                                       'keyboard')
clicker_upgrade_keyboard.add(clicker_upgrade_mechanical_keyboard)

clicker_upgrade_auto_clicker = types.InlineKeyboardButton(f'auto clicker', callback_data='auto clicker')
clicker_upgrade_keyboard.add(clicker_upgrade_auto_clicker)

# Подставить в ф строки выражения из test.py
