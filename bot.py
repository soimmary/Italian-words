import telebot
import italian

TOKEN = '997358493:AAH2Hn57D3yFXgNh90lvQYrPzjPogVmIEqs'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'cтартовое сообщение')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '\ciao или ciao – спрошу слово')


@bot.message_handler(commands=['ciao'])
def ciao_message(message):
    if str(message.text).strip().lower() not in ['sonostanco', 'sono stanco', 'яустал', 'я устал']:
        word, number = italian.askItalianWord()
        bot.send_message(message.chat.id, word)
        bot.register_next_step_handler(message=message, callback=ciao_message_main, number=number)


def ciao_message_main(message, number: int):
    if str(message.text).strip().lower() not in ['sonostanco', 'sono stanco', 'яустал', 'я устал']:
        usersAnswer = str(message.text).lower()
        myDecision = italian.answerItalianWord(usersAnswer, number)
        bot.send_message(message.chat.id, myDecision)
        word, number = italian.askItalianWord()
        bot.send_message(message.chat.id, word)
        bot.register_next_step_handler(message=message, callback=ciao_message_main, number=number)


@bot.message_handler(commands=['paroleNuove'])
def parole_nuove(message):
    instructions = 'Inserisci la parola italiana e la parola russa.\nPer esempio: cioccolato - шоколад.'
    bot.send_message(message.chat.id, instructions)
    bot.register_next_step_handler(message=message, callback=parole_nuove_main)


def parole_nuove_main(message):
    italian.newWordsWithStr(wordNtranslation=str(message.text))
    bot.send_message(message.chat.id, 'added')


@bot.message_handler(commands=['saveWords'])
def save_words(message):
    italian.save()
    doc = open('words.txt', 'r')
    bot.send_document(message.chat.id, doc)

@bot.message_handler(content_types=['text'])
def ciao_text_message(message):
    if str(message.text).lower() == 'ciao':
        ciao_message(message)
    else:
        bot.send_message(message.chat.id, 'я не знаю таких команд /help')


bot.polling(none_stop=True)