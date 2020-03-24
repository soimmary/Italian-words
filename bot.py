import telebot
import os
import italian

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])  # decorator
def start_message(message):
    user_id = message.chat.id
    italian.MODELLO_BY_ID[user_id] = 'ital -> rus'
    bot.send_message(message.chat.id, 'CIAO!')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/ciao o ciao – damando la parola\n'
                                      '/sonostanco o sonostanco – ')


@bot.message_handler(commands=['modello'])
def modello_message(message):
    keyboard_modello = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_modello.row('ital -> rus', 'rus -> ital')
    bot.send_message(message.chat.id, 'Scegli il modello', reply_markup=keyboard_modello)
    bot.register_next_step_handler(message, modello_message_register_modello)


def modello_message_register_modello(message):
    user_id = message.chat.id
    user_choice = str(message.text).strip().lower()
    if user_choice in ('ital -> rus', 'rus -> ital'):
        italian.MODELLO_BY_ID[user_id] = user_choice
        bot.register_next_step_handler(message, ciao_message_ask)
    else:
        bot.send_message(message.chat.id, "l'errore")
        bot.register_next_step_handler(message, modello_message)


@bot.message_handler(commands=['ciao'])
def ciao_message_ask(message, is_first_call=True):
    if str(message.text).strip().lower() not in ('sonostanco', 'sono stanco'):  # proverka na ustalost'
        user_id = message.chat.id
        word = italian.choose_word()
        if italian.MODELLO_BY_ID[user_id] == 'ital -> rus':
            bot.send_message(message.chat.id, word[0])
        elif italian.MODELLO_BY_ID[user_id] == 'rus -> ital':
            bot.send_message(message.chat.id, word[1])
        bot.send_message(message.chat.id, 'aspetto la tua risposta')
        bot.register_next_step_handler(message, ciao_message_check_answer, word=word)
    else:
        sonostanco_message(message)


def ciao_message_check_answer(message, word):
    answer = str(message.text).strip().lower()
    if answer not in ('sonostanco', 'sono stanco'):
        user_id = message.chat.id
        my_decision = italian.check_answer(answer, word, user_id)
        bot.send_message(message.chat.id, my_decision)
        ciao_message_ask(message)
    else:
        sonostanco_message(message)


@bot.message_handler(commands=['sonostanco'])
def sonostanco_message(message):
    bot.send_message(message.chat.id, 'hai lavorato bene!')


@bot.message_handler(content_types=['text'])
def ciao_text_message(message):
    if str(message.text).strip().lower() == 'ciao':
        ciao_message_ask(message)
    elif str(message.text).strip().lower() == 'modello':
        modello_message(message)
    else:
        bot.send_message(message.chat.id, 'non so questo comando')


bot.polling(none_stop=True)
