import telebot
import keyboards as kb
import json_functions as jf
import time
import blackjack as bj


bot = telebot.TeleBot("key")

expansion_constants = {
    'auto': {
      'calculator': 1, 'video card': 1, 'pc': 1, 'video card stand': 1, 'quantum computer': 1, 'data center': 1
    },
    'click': {
        'new mouse': 1, 'new keyboard': 1, 'mechanical keyboard': 1, 'auto clicker': 1
    }
}


@bot.message_handler(commands=['start'])
def start(message):
    data = jf.download_data()
    user = {message.from_user.username: {'money': 0, 'expansions': {'auto': {}, 'clicker': {}}, 'is_Running': False},
            'chat_id': message.chat.id}
    data.update(user)
    jf.load_data(data)


@bot.message_handler(commands=['clicker'])
def clicker(message):
    bot.send_message(message.chat.id, 'clicker summoned', reply_markup=kb.clicker_keyboard)


@bot.message_handler(commands=['click!'])
def add_money(message):
    data = jf.download_data()
    data[message.from_user.username]['money'] += 1
    print(message.chat.id)
    jf.load_data(data)


@bot.message_handler(commands=['upgrade_click'])
def click_upgrade(message):
    bot.send_message(message.chat.id, 'choose upgrade:', reply_markup=kb.clicker_upgrade_keyboard)


@bot.message_handler(commands=['upgrade_auto'])
def auto_upgrade(message):
    bot.send_message(message.chat.id, 'choose upgrade:', reply_markup=kb.auto_upgrade_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(callback):
    data = jf.download_data()

    try:
        new_values = {callback.data: data[callback.from_user.username]['expansions'][callback.data] + 1}
    except KeyError:
        if callback.data in expansion_constants['auto']:
            new_values = {callback.data: 1}
        else:
            new_values = {callback.data: 1}

    if callback.data in expansion_constants['auto']:
        data[callback.from_user.username]['expansions']['auto'].update(new_values)
    else:
        data[callback.from_user.username]['expansions']['clicker'].update(new_values)
    jf.load_data(data)

    if callback.data in expansion_constants['auto'] and not data[callback.from_user.username]['is_Running']:
        data[callback.from_user.username]['is_Running'] = True
        jf.load_data(data)
        msg = bot.send_message(callback.message.chat.id, 'starting auto mining')
        bot.register_next_step_handler(msg, get_auto_money(callback.from_user))


@bot.message_handler(commands=['blackjack'])
def blackjack(message):
    if len(message.text) == 10:
        msg = bot.send_message(message.chat.id, 'you started blackjack vs computer croupier')
        bot.register_next_step_handler(msg, solo_blackjack())
        return None
    else:
        players_nicknames = message.text.split()
        del players_nicknames[0]
        data = jf.download_data()
        players_info = {message.from_user.username: {'message_id': message.chat.id}}
        for i in players_nicknames:
            if data.get(i) is None:
                bot.send_message(message.chat.id, 'player that was mentioned are not playing clicker at all')
                return None
            players_info_to_add = {i: {'message_id': data.get(i)['message_id']}}
            players_info.update(players_info_to_add)
        msg = bot.send_message(message.chat.id, 'blackjack starting!')
        bot.register_next_step_handler(msg, blackjack_main(players_nicknames, players_info))


@bot.message_handler(commands=['blackjack_bet'])
def blackjack_bet(message):
    try:
        bet = int(message.text[15:])

    except TypeError:
        bot.send_message(message.chat.id, 'bet must be integer')


@bot.message_handler(commands=['top'])
def top(message):
    pass


def get_auto_money(message):
    while True:
        data = jf.download_data()
        for i in expansion_constants['auto']:
            if i in data[message.username]['expansions']['auto']:
                data[message.username]['money'] += expansion_constants['auto'][i] * \
                                                             data[message.username]['expansions']['auto'][i]

        jf.load_data(data)
        time.sleep(10)


def solo_blackjack():
    pass


def blackjack_main(players_nicknames, players_info):
    players = len(players_nicknames)
    card_pool = [4 * (1 + players // 6)] * 13
    players_info.update({'croupier': {'cards': bj.get_cards(card_pool)}})

    for i in players_nicknames:
        player_cards = {i: {'cards': bj.get_cards(card_pool)}}

        players_info.update(player_cards)


while True:
    try:
        bot.polling()
    except BaseException:
        time.sleep(15)
