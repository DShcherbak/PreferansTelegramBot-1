import telebot
import config
import preferans

bot = telebot.TeleBot(config.Token)
id_list = []
count_id = 0
Preferans = preferans.Preferans()


@bot.message_handler(commands=['start'])
def start_messaging(message):
    global count_id
    bot.send_message(message.from_user.id, 'Ты в игре!')
    id_list.append(message.from_user.id)
    count_id += 1
    if count_id == config.cnt_players:
        new_round()


def new_round():
    Preferans.set_round()
    bot.send_message(id_list[0], 'Твои карты:\n' + hand_to_string(Preferans.hand0()))
    bot.send_message(id_list[1], 'Твои карты:\n' + hand_to_string(Preferans.hand1()))
    bot.send_message(id_list[2], 'Твои карты:\n' + hand_to_string(Preferans.hand2()))
    ask_bidding()


@bot.message_handler(func=lambda message: config.state == 'bidding')
def bidding(message):
    if message.from_user.id != id_list[Preferans.current_player()] :
        bot.send_message(message.from_user.id, 'Имей терпение, блэт!')
    elif message.text != '+' and message.text != '-' and message.text != 'мизер':
        bot.send_message(message.from_user.id, 'Неккоректные входные данные')
    else:
        type_answer = 0
        if message.text == '+':
            type_answer = 1
        if message.text == '-':
            type_answer = 3
        if message.text == 'мизер':
            type_answer = 2
        if Preferans.update_bidding(type_answer):
            ask_bidding()
            print(Preferans.current_player())


@bot.message_handler(func=lambda message: config.state != 'bidding')
def hz(message):
    print('asdsadsa')


def hash_to_sting(_hash):
    answer = ''
    if _hash // 4 <= 10:
        answer += str(_hash // 4)
    elif _hash // 4 == 11:
        answer += 'J'
    elif _hash // 4 == 12:
        answer += 'Q'
    elif _hash // 4 == 13:
        answer += 'K'
    elif _hash // 4 == 14:
        answer += 'A'
    if _hash % 4 == 0:
        answer += '♠'
    elif _hash % 4 == 1:
        answer += '♣'
    elif _hash % 4 == 2:
        answer += '♦'
    elif _hash % 4 == 3:
        answer += '♥'
    return answer


def hand_to_string(hand):
    answer = ''
    last_suit = -1
    for i in hand:
        if last_suit != - 1 and last_suit != i % 4:
            answer += '\n'
        answer += hash_to_sting(i)
        answer += ' '
        last_suit = i % 4
    return answer


def ask_bidding():
    bot.send_message(id_list[Preferans.current_player()], 'Ваше слово!!\nМинимальная ставка - '
                     + hash_to_sting(Preferans.dib()) + 'Отправь "+" если хочешь играть, '
                                                        '"-" если хочешь пасануть и "мизер" если хочешь сказать мизер\n')


bot.polling()
