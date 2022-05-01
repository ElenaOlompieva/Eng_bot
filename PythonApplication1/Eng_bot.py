import telebot
import time
import random

# Токен, который выдает @botfather
bot = telebot.TeleBot('')
# ИД чата в телеграме
CHANNEL_NAME = ''
# Загружаем список английских слов
f = open('En_words.txt', 'r', encoding='UTF-8')
NewWords = f.read().split('\n')
f.close()

a = len(NewWords)

while a > 0:
    #Пока не закончатся слова, посылаем их в канал
    NewWord = random.choice(NewWords)
    #Удялем из списка элемент, который выбрали для отправки в чат, чтобы не отправить его повторно
    NewWords.remove(NewWord)
    #Делим строку на отдельные части: слово и его перевод
    n1, n2 = map(str, NewWord.split('-'))
    #Добавляем форматирование текста
    NewWord = "<b>" + n1 + "</b>" + "-" + "<em>" + n2 + "</em>"
    #Отправляем сообщение в чат
    bot.send_message(CHANNEL_NAME, NewWord, parse_mode = "HTML")
    #Часовая пауза для отправки сообщения
    time.sleep(3600)
    a = a - 1
else:
    bot.send_message(CHANNEL_NAME, "Слова закончились :(")


