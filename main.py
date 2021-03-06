import socket
from datetime import time

import requests
import urllib3
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from blacklist import bs_ds, bs_nick, bs_id
from donates import donates
from discords import discords
from nicknames import nicknames
from config import vk_token
from data import db_session
from bad_words import bad

sessionStorage = {}


def main():
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    vk_session = vk_api.VkApi(
        token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, 195012202)

    while True:
        try:
            for event in longpoll.listen():

                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    print('Новое сообщение:')
                    print('Для меня от:', event.obj.message['from_id'])
                    print('Текст:', event.obj.message['text'])
                    handle_dialog(event, vk)

        except (requests.exceptions.ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError):
            print('n_____________Timeout______________n')


def handle_dialog(event, vk):
    rndm = random.randint(0, 2 ** 64)
    user_id = event.obj.message['from_id']
    message = event.obj.message['text']
    if str(user_id) in bs_id:
        vk.messages.send(user_id=user_id,
                         message=f"Ваш аккаунт ВКонтакте недоступен для подачи "
                                 f"заявок в клан. Если Вы хотите узнать причину, "
                                 f"пишите сюда:\n"
                                 f"-> @xskywalker",
                         random_id=rndm)
    if 'принять' in message.lower().split() and user_id == 570864703:
        vk.messages.send(user_id=message.lower().split()[1],
                         message=f"Congratulations!!!🎉🎉🎉\n"
                                 f"✅Вы приняты в клан Harakiri!\n"
                                 f"Скоро Вас добавят в беседу клана 🔥",
                         random_id=rndm)
    elif 'принять' not in message.lower().split() and user_id == 570864703:
        splited = message.split()
        id = splited[-1]
        del splited[-1]
        message = ' '.join(splited)
        vk.messages.send(user_id=id,
                         message=f"🚫К сожалению, Ваша заявка была отклонена.\n"
                                 f"Причина: {message}",
                         random_id=rndm)

    if user_id in sessionStorage:
        quests = sessionStorage[user_id]['last_question']
        if quests == 1:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            vk.messages.send(user_id=user_id,
                             message=f"Добро пожаловать, {message}! \n"
                                     f"Теперь напишите свой nickname на мини-играх",
                             random_id=rndm)
            sessionStorage[user_id]['last_question'] = 2
            sessionStorage[user_id]['id'] = user_id
            return

        if quests == 2:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return
            if message.lower() in bs_nick:
                vk.messages.send(user_id=user_id,
                                 message=f"Ваш никнейм находится в черном списке клана\n"
                                         f"Ваша заявка автоматически отклонена.",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 0
                return
            elif message.lower() in nicknames:
                vk.messages.send(user_id=user_id,
                                 message="Этот никнейм уже зарегистрирован",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 2
                return
            flag = True
            while flag:
                message_splited = list(message)
                print(message_splited)
                for element in message_splited:
                    if element in "1234567890_qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
                        flag = True
                    else:
                        flag = False
                        vk.messages.send(user_id=user_id,
                                         message="Никнейм содержит неприемлемые символы. Повторите попытку.",
                                         random_id=rndm)
                        sessionStorage[user_id]['last_question'] = 2
                        return
                vk.messages.send(user_id=user_id,
                                 message=f"Отлично! Введите Ваш реальный возраст😎\n"
                                         f"(Внимание! Не преувеличивайте свой возраст, этот вопрос задан для того, "
                                         f"чтобы мы имели представление о Вас. Это не повлияет на то, "
                                         f"одобрим ли мы Вашу заявку или нет.)\n"
                                         f"!!! Пишите свой возраст цифрами, иначе бот не поймет Вас !!!",
                                 random_id=rndm)
                sessionStorage[user_id]['nick'] = message
                sessionStorage[user_id]['last_question'] = 3
                return

        if quests == 3:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return

            if message.isdigit() and 6 < int(message) < 30:
                vk.messages.send(user_id=user_id,
                                 message=f"Хорошо! Теперь укажите Ваш донат на мини-играх.🤑\n"
                                         f"Пишите донат английскими символами! Если доната нет, "
                                         f"напишите 'player'",
                                 random_id=rndm)
                sessionStorage[user_id]['age'] = message
                sessionStorage[user_id]['last_question'] = 4
                return
            else:
                vk.messages.send(user_id=user_id,
                                 message=f"Не пытайтесь меня обмануть😡 \n"
                                         f"Введите свой реальный возраст.",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 3
                return

        if quests == 4:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return

            if message.lower() in donates:
                vk.messages.send(user_id=user_id,
                                 message=f"Отлично! Теперь напишите свой дискорд.😴 Если у Вас его нет, то советуем "
                                         f"зарегистрироваться, а пока что напишите боту 'нет' \n"
                                         f"Пример никнейма в дискорде: Snowylqrd#1100",
                                 random_id=rndm)
                sessionStorage[user_id]['donate'] = message
                sessionStorage[user_id]['last_question'] = 5
                return
            else:
                vk.messages.send(user_id=user_id,
                                 message=f"Вы должны ввести существующий донат английскими буквами!🤬",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 4
                return

        if quests == 5:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return
            message_listed = list(message)
            if message.lower() in bs_ds:
                vk.messages.send(user_id=user_id,
                                 message=f"Ваш дискорд находится в черном списке клана\n"
                                         f"Ваша заявка автоматически отклонена.",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 0
                return
            elif message.lower() == 'нет':
                vk.messages.send(user_id=user_id,
                                 message=f"Хорошо. Оцените, сколько часов в день вы можете"
                                         f"уделять нашему клану🥺 (Имеется в виду не только время,"
                                         f"потраченное на мини-играх, но и активное участие"
                                         f"в беседе/группе/дискорде клана.)"
                                         f"!!! Пишите количество часов цифрами, иначе бот не поймет Вас !!!",
                                 random_id=rndm)
                sessionStorage[user_id]['discord'] = message
                sessionStorage[user_id]['last_question'] = 6
                return
            elif message.lower() in discords:
                vk.messages.send(user_id=user_id,
                                 message=f"Не обманывайте меня👿\n"
                                         f"Этот дискорд уже зарегистрирован",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 5
                return
            elif '#' in message and message_listed[-1].isdigit() and message_listed[-2].isdigit() and \
                    message_listed[-3].isdigit() and message_listed[-4].isdigit():
                vk.messages.send(user_id=user_id,
                                 message=f"Amazing! Оцените, сколько часов в день вы можете "
                                         f"уделять нашему клану🥺 (Имеется в виду не только время, "
                                         f"потраченное на мини-играх, но и активное участие"
                                         f"в беседе/группе/дискорде клана.)\n"
                                         f"!!! Пишите количество часов цифрами, иначе бот не поймет Вас !!!",
                                 random_id=rndm)
                sessionStorage[user_id]['discord'] = message
                sessionStorage[user_id]['last_question'] = 6
                return
            else:
                vk.messages.send(user_id=user_id,
                                 message=f"Не обманывайте меня👿\n"
                                         f"Введите свой реальный никнейм в дискорде",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 5
                return

        if quests == 6:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return

            if message.isdigit() and int(message) > 24:
                vk.messages.send(user_id=user_id,
                                 message=f"Вздумали обмануть меня?😒\n"
                                         f"В сутках всего-лишь 24 часа!\n"
                                         f"Повторите попытку.",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 6
                return
            else:
                vk.messages.send(user_id=user_id,
                                 message=f"Well! Осталось еще чуть-чуть😉\n\n"
                                         f"В каких кланах Вы раньше были?",
                                 random_id=rndm)
                sessionStorage[user_id]['hours'] = message
                sessionStorage[user_id]['last_question'] = 7
                return

        if quests == 7:
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return

            vk.messages.send(user_id=user_id,
                             message=f"Wonderful!😏 Отправьте скриншот Вашей статистики на режиме "
                                     f"'BedWars'",
                             random_id=rndm)
            sessionStorage[user_id]['clans'] = message
            sessionStorage[user_id]['last_question'] = 8
            return

        if quests == 8:
            if message == '/сбросить':
                vk.messages.send(user_id=user_id,
                                 message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                         f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                         f" иначе Ваша заявка "
                                         f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                         f"Желаем вам удачи на отборе!)\n"
                                         f"C уважением, @xskywalker"
                                         f"\n\n"
                                         f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                         f"\n\n"
                                         f"Итак, приступим. \n"
                                         f"Как к вам можно обращаться? (Напишите свое имя)",
                                 random_id=rndm)
                sessionStorage[user_id] = {
                    'last_question': 1
                }
                return
            message_bad = message.split()
            for el in message_bad:
                if el in bad:
                    vk.messages.send(user_id=user_id,
                                     message=f"Ваша заявка автоматически отклонена😭\n"
                                             f"Причина: оскорбительное поведение",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 0
                    return

            vk.messages.send(user_id=user_id,
                             message=f"Поздравляем!🥳\n Ваша заявка была отправлена на рассмотрение "
                                     f"администрации клана.\n"
                                     f"⚠ Примерное время ожидания составляет ~ 1 день",
                             random_id=rndm)

            vk.messages.send(user_id=570864703,
                             message=f"У вас новая заявка от @id{user_id}\n"
                                     f"1. [Ник] {sessionStorage[user_id]['nick']}\n"
                                     f"2. [Донат] {sessionStorage[user_id]['donate']}\n"
                                     f"3. [Возраст] {sessionStorage[user_id]['age']}\n"
                                     f"4. [Дискорд] {sessionStorage[user_id]['discord']}\n"
                                     f"5. [Часов в день] {sessionStorage[user_id]['hours']}\n",
                             random_id=rndm)
            sessionStorage[user_id]['last_question'] = 9
            return

    else:
        vk.messages.send(user_id=user_id,
                         message=f"Вас приветствует Harakiri-bot. Чтобы заполнить заявку,"
                                 f"отвечайте на вопросы, которые задаст бот. Помните, пишите только реальные данные,"
                                 f" иначе Ваша заявка "
                                 f"будет отклонена. Если Вы нашли ошибку, пишите напрямую создателю клана.\n"
                                 f"Желаем вам удачи на отборе!)\n"
                                 f"C уважением, @xskywalker"
                                 f"\n\n"
                                 f"если вы случайно допустили ошибку в заполнении, напишите '/сбросить'"
                                 f"\n\n"
                                 f"Итак, приступим. \n"
                                 f"Как к вам можно обращаться? (Напишите свое имя)",
                         random_id=rndm)
        sessionStorage[user_id] = {
            'last_question': 1
        }
        return


if __name__ == '__main__':
    main()
