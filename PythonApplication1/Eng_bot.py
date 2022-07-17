import telebot
import time
import random
import sqlite3
from datetime import datetime

#Токен, который выдает @botfather
bot = telebot.TeleBot('')
#ИД чата в телеграме
CHANNEL_NAME = ''
#Загружаем список английских слов
f = open('En_words.txt', 'r', encoding='UTF-8')
NewWords = f.read().split('\n')
f.close() 

#Проверка перед вставкой: есть ли слово в таблице English_Words
def check_varible (Word):
    sqlite_connection = sqlite3.connect('English_words.db')
    cursor = sqlite_connection.cursor()

    check = cursor.execute('SELECT * FROM English_Words WHERE Word=?', (Word, ))
    if check.fetchone() is None: 
        return 0
    else:
        return 1
    cursor.close()

#Вставка нового слова в таблицу English_Words
def insert_varible_into_table (Word, Translation):
    sqlite_connection = sqlite3.connect('English_words.db')
    cursor = sqlite_connection.cursor()

    sqlite_insert_with_param = """INSERT INTO English_Words (Word, Translation)
                                  VALUES (?, ?);"""

    data_tuple = (Word, Translation)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()

    cursor.close()

a = len(NewWords)
#Цикл для вставки данных в таблицу
while a > 0:
    #Берем первый элемент из списка
    NewWord = NewWords[0]
    #Удялем из списка элемент, который выбрали для отправки в чат, чтобы не отправить его повторно
    NewWords.remove(NewWord)
    #Делим строку на отдельные части: слово и его перевод
    n1, n2 = map(str, NewWord.split('--'))
    #Очистка от лишних пробелов
    n1 = n1.lstrip()
    n2 = n2.lstrip()
    n1 = n1.rstrip()
    n2 = n2.rstrip()
    #Перед вставкой проверяем есть ли слово в таблице. Если отсутствует - добавляем
    if check_varible(n1) == 0:
        insert_varible_into_table(n1, n2)

    a = a - 1

#Выбор слова для отправки из таблицы English_Words
#Проверяем, чтобы слово не было отправлено в чат ранее
def select_word (CHANNEL_NAME):
    sqlite_connection = sqlite3.connect('English_words.db')
    cursor = sqlite_connection.cursor()

    cursor.execute("""SELECT *
                        FROM(SELECT w.Word_ID, w.Word, w.Translation
                               FROM English_Words AS w
  
                             EXCEPT

                             SELECT w.Word_ID, w.Word, w.Translation
                               FROM English_Words AS w  
                               JOIN Log_English_Words as lw
                                 ON lw.Word_ID = w.Word_ID
                              WHERE lw.Chat_ID = ?) AS p
                              ORDER BY RANDOM() LIMIT 1""", (CHANNEL_NAME, ))

    result = cursor.fetchall()

    return result
    cursor.close()

#Вставка записи в таблицу с логами Log_English_Words 
def insert_log (WordID, ChatID, Date_value):
    sqlite_connection = sqlite3.connect('English_words.db')
    cursor = sqlite_connection.cursor()

    sqlite_insert_with_param = """INSERT INTO Log_English_Words (Word_ID, Chat_ID, Date_value)
                                  VALUES (?, ?, ?);"""

    data_tuple = (WordID, ChatID, Date_value)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()

    cursor.close()

#Выбираем рандомное слово из таблицы English_Words для отправки
result = select_word(CHANNEL_NAME)

#цикл для отправки слов 
while len(result) > 0 :
    #Присваиваем значения переменным из списка
    Word_ID = result[0][0]
    Word = result[0][1]
    Translation = result[0][2]
    #Тек.дата для логирования
    DatetimeNow = datetime.now()

    #логируем отправленное слово
    insert_log(Word_ID, CHANNEL_NAME, DatetimeNow)
    #Выбираем новое слово
    result = select_word(CHANNEL_NAME)

    #Добавляем форматирование текста, формируем сообщение для отправки
    NewWord = "<b>" + Word + "</b>" + " - " + "<em>" + Translation + "</em>"
    #Отправляем сообщение в чат
    bot.send_message(CHANNEL_NAME, NewWord, parse_mode = "HTML")
    #Часовая пауза для отправки сообщения
    time.sleep(3600)

else:
    bot.send_message(CHANNEL_NAME, "Слова закончились :(")




