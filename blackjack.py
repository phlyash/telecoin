import random


def get_cards(card_pool):
    cards = [random.randint(0, 12), random.randint(0, 12)]

    while True:
        if not card_pool[cards[0]] == 0 or not card_pool[cards[1]] == 0:
            card_pool[cards[0]] -= 1
            card_pool[cards[1]] -= 1
            return cards
        cards = [random.randint(0, 12), random.randint(0, 12)]


def croupier(dealer, card_pool):
    while sum_cards(dealer) < 17:
        dealer = hit(dealer, card_pool)
        dealer = ace_change(dealer)


def card_value(card):
    if 0 <= card <= 8:
        return card + 2
    elif 9 <= card <= 11:
        return 10
    elif card == 12:
        return 11
    else:
        return 1


def game_checker(cards):
    if sum_cards(cards) > 21 and not len(cards) == 2:
        raise Exception('Card sum more than 21')


def sum_cards(cards):
    answer = 0
    cards = ace_change(cards)

    for i in range(len(cards)):
        answer += card_value(cards[i])

    return answer


def number_to_card(card):
    if 0 <= card <= 8:
        return str(card + 2)

    elif card == 9:
        return 'jack'

    elif card == 10:
        return 'queen'

    elif card == 11:
        return 'king'

    return 'ace'


def ace_change(cards):
    cards_sum = 0

    for i in range(len(cards)):
        cards_sum += card_value(cards[i])

    if 12 in cards:
        if cards_sum > 21 and len(cards) != 2:
            cards[cards.index(12)] = 13
    return cards


def hit(cards, card_pool):
    new_card = random.randint(0, 12)

    while True:
        if not card_pool[new_card] == 0:
            card_pool[new_card] -= 1
            cards.append(new_card)
            return cards
        new_card = random.randint(0, 12)


def split(cards, card_pool):
    answer = {}

    for i in range(2):
        new_card = {f'cards{i}': hit([cards[i]], card_pool)}
        answer.update(new_card)
    return answer


def double(cards, card_pool):
    new_card = random.randint(0, 12)

    while True:
        if not card_pool[new_card] == 0:
            card_pool[new_card] -= 1
            cards.append(new_card)
            return {'cards': cards}
        new_card = random.randint(0, 12)


def possibilities(cards, split_check):
    answer = ['hit', 'double', 'surrender', 'stand']  # cant sur when take 1 card

    if card_value(cards[0]) == card_value(cards[1]) and not split_check:
        answer.append('split')

    return answer


def end_game(croupier_sum, players, croupier_in_range, players_nicknames, players_info):
    answer = {}

    for i in range(players):
        deck_amount = 1
        try:
            player = players_info[players_nicknames[i]][f'cards{0}']
            deck_id = 0
            deck_amount += 1
        except KeyError:
            player = players_info[players_nicknames[i]]['cards']
            deck_id = ''

        for j in range(deck_amount):
            player_in_range = sum_cards(player) <= 21 or (sum_cards(player) == 2 and len(player) == 2)
            if croupier_sum < sum_cards(players_info[players_nicknames[i]][f'cards{deck_id}']) and player_in_range or \
                    not croupier_in_range and player_in_range:
                player_result = {players_nicknames[i]: 'win'}
                answer.update(player_result)

            elif not player_in_range and not croupier_in_range or \
                    sum_cards(player) == sum_cards(players_info['croupier'][f'cards{deck_id}']):
                player_result = {players_nicknames[i]: 'draw'}
                answer.update(player_result)

            elif sum_cards(players_info['croupier'][f'cards{deck_id}']) > sum_cards(player) and croupier_in_range or \
                    not player_in_range:
                player_result = {players_nicknames[i]: 'lose'}
                answer.update(player_result)

            deck_id = 1

            try:
                player = players_info[players_nicknames[i]][f'cards{j}']
            except KeyError:
                continue

    return answer


def player_start(player, split_check, deck_id, players_info):
    player_possibilities = possibilities(players_info[player][f'cards{deck_id}'], split_check)
    print(player, 'you have:', *[number_to_card(k) for k in players_info[player][f"cards{deck_id}"]])
    player_choice = input(f'{player} choice your move from this options: ' + ' '.join(player_possibilities)
                          + ' ')

    while player_choice not in player_possibilities:
        player_choice = input('wrong command, choice from this options: ' + ' '.join(player_possibilities)
                              + ' ')
    return player_choice


def action(player_choice, player, deck_id, players_info, card_pool):
    try:
        if player_choice == 'hit':
            players_info[player]['cards'] = hit(players_info[player][f'cards{deck_id}'], card_pool)
            game_checker(players_info[player][f'cards{deck_id}'])
            action(player_start(player, False, '', players_info), player, deck_id, players_info, card_pool)

        if player_choice == 'surrender' and len(players_info[player][f'cards{deck_id}']) == 2:
            players_info[player]['bet'] /= 2

        if player_choice == 'stand':
            raise Exception('stand')

        if player_choice == 'double':
            players_info[player]['bet'] *= 2
            players_info[player].update(double(players_info[player]['cards'], card_pool))

        if player_choice == 'split':
            players_info[player].update(split(players_info[player]['cards'], card_pool))
            players_info[player].pop('cards')

            for j in range(2):
                player_choice = player_start(player, True, j, players_info)
                game_checker(players_info[player][f'cards{j}'])
                action(player_choice, player, j, players_info, card_pool)

    except Exception:
        return

    return players_info


def main():
    players = int(input())
    players_nicknames = []
    card_pool = [4 * (1 + players // 6)] * 13

    players_info = {'croupier': {'cards': get_cards(card_pool)}}

    for i in range(players):
        player_cards = {f'player {i+1}': {'cards': get_cards(card_pool), 'bet': int(input('place your bet: '))}}
        players_nicknames.append(f'player {i+1}')
        players_info.update(player_cards)

    print(f"croupier has: {number_to_card(players_info['croupier']['cards'][0])}, UNKNOWN")

    for i in range(players):
        player = players_nicknames[i]

        player_choice = player_start(player, False, '', players_info)

        action(player_choice, player, '', players_info, card_pool)

    croupier(players_info['croupier']['cards'], card_pool)
    croupier_sum = sum_cards(players_info['croupier']['cards'])
    croupier_in_range = croupier_sum <= 21 or (croupier_sum == 22 and len(players_info['croupier']['cards']) == 2)

    game_result = end_game(croupier_sum, players, croupier_in_range, players_nicknames, players_info)

    j = 0
    for i in game_result.items():
        print(f'player {j+1} {i[1]}')
        j += 1


if __name__ == '__main__':
    main()
