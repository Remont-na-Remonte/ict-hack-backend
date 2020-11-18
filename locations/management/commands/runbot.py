#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from bot.models import TelegramUser
import telebot
from telebot import types
import requests
from django.conf import settings
import sys
sys.path.append(settings.BASE_DIR)
import config

keybord_geo = telebot.types.ReplyKeyboardMarkup(True, True)
keybord_ans = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_next = telebot.types.ReplyKeyboardMarkup(True, True)

button_next = types.KeyboardButton(text="Выбрать следующий объект")
button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
button_ans = types.KeyboardButton(text="Оставить отзыв о месте")

keybord_geo.add(button_geo)
keybord_ans.add(button_ans)
keyboard_next.add(button_next)

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN, parse_mode=None)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def chose_objects(chatid):
            #TODO get list of objec form db
            # list << req to server
            # longitude': 37.400234, 'latitude
            bot.send_message(chatid, 
            "Твои объекты:\n1. ул Тверская (посмотреть объект www.link1.ru)\n2. ул Маяковская (посмотреть объект www.link1.ru)\n3. ул Пушкина (посмотреть объект www.link1.ru)\n4. ул Есенина (посмотреть объект www.link1.ru)\n5 ул Толстого (посмотреть объект www.link1.ru)\n\nТвой маршрут:"
            )
            bot.send_message(chatid, "Выбери объект проверки")
            #add list to object_list


        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, "Напиши мне что-нибудь!")


        @bot.message_handler(content_types=['location'])
        def handle_loc(message):
            chatid = message.chat.id
            user, created = TelegramUser.objects.get_or_create(bot_chatid=chatid)
            if user.bot_state == 2:
                print(message.location)
                #TODO Send coords to server and write answer to db
                chose_objects(chatid)


        @bot.message_handler(content_types=['photo'])
        def save_photo(message):
            chatid = message.chat.id
            user, created = TelegramUser.objects.get_or_create(bot_chatid=chatid)
            if user.bot_state == 5:
                fileID = message.photo[-1].file_id
                file = bot.get_file(fileID)
                user.photo_path = file.file_path
                user.save()
                bot.send_message(chatid, "Оставьте комментарий")

        @bot.message_handler(content_types=['text'])
        def echo_all(message):
            chatid = message.chat.id
            
            user, created = TelegramUser.objects.get_or_create(bot_chatid=chatid)
            Chat_status = user.bot_state 

            print(Chat_status)
            if Chat_status > 5:
                Chat_status = 6
    
            elif Chat_status == 1:
                bot.reply_to(
                    message, 
                    "Пришли свои координаты для нахождения объектов неподалеку :)",
                    reply_markup=keybord_geo
                )
    
            elif Chat_status == 2:
                #TODO check if user have object list
                #TODO get data from database
                bot.send_message(chatid, 'Вы выбрали "ул Маяковская"\nМаршрут:')
                bot.send_message(
                    chatid, 
                    "https://yandex.ru/maps/?rtext=" + 
                    str(59.87) + "," + 
                    str(30.27) +
                    "~59.898495,30.299559&rtt=mt",
                    reply_markup=keybord_ans
                )
                bot.send_message(chatid, "Напиши, когда будетшь готов оставить отзыв о объекте :)")

            elif Chat_status == 3:
                bot.reply_to(message, 
                        "Оставьте балл, который описывает состояние (от 1 до 10)")
    
            elif Chat_status == 4:
                try:
                    int(message.text)
                except:
                    bot.send_message(chatid, "Некорректное значение")
                    Chat_status -= 1
                    return

                score = int(message.text)
        
                if score > 10 or score < 1:
                    bot.send_message(chatid, "Значение вне диапозона")
                    Chat_status -= 1
                    return
                user.object_score = score
                bot.reply_to(message, "Оставьте фото")
    
            elif Chat_status == 5:
                user.comment = message.text
                bot_text = "Проверка выполнена!\nПосмотрите отчет о вашей проверке по объекту 1. ул Тверская по ссылке www.link1.ru"
                bot.reply_to(message, bot_text, reply_markup=keyboard_next)

            Chat_status += 1
            user.bot_state = Chat_status
            user.save()

        bot.polling()
