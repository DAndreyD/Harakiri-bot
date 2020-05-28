import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from config import vk_token
from data import db_session

sessionStorage = {}


def main():
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    vk_session = vk_api.VkApi(
        token=vk_token)
    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, 195012202)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            handle_dialog(event, vk)


def handle_dialog(event, vk):
    rndm = random.randint(0, 2 ** 64)
    user_id = event.obj.message['from_id']
    message = event.obj.message['text']
    if user_id in sessionStorage:
        quests = sessionStorage[user_id]['last_question']
        if quests == 1:
            vk.messages.send(user_id=user_id,
                             message=f"Добро пожаловать, {message}! \n"
                                     f"Теперь напишите свой nickname на мини-играх",
                             random_id=rndm)
            sessionStorage[user_id]['last_question'] = 2
            return

        if quests == 2:
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
                sessionStorage[user_id]['last_question'] = 3
                return

        if quests == 3:
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
            message_splited = list(message)
            for element in message_splited:
                if element in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
                    vk.messages.send(user_id=user_id,
                                     message=f"Отлично! Теперь напишите свой дискорд.😴 Если у Вас его нет, то советуем "
                                             f"зарегистрироваться, а пока что напишите боту 'нет' \n"
                                             f"Пример никнейма в дискорде: Snowylqrd#1100",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 5
                    return
                else:
                    vk.messages.send(user_id=user_id,
                                     message=f"Вы должны ввести донат английскими буквами!🤬",
                                     random_id=rndm)
                    sessionStorage[user_id]['last_question'] = 4
                    return

        if quests == 5:
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
            if message.lower() == 'нет':
                vk.messages.send(user_id=user_id,
                                 message=f"Хорошо. Оцените, сколько часов в день вы можете"
                                         f"уделять нашему клану🥺 (Имеется в виду не только время,"
                                         f"потраченное на мини-играх, но и активное участие"
                                         f"в беседе/группе/дискорде клана.)"
                                         f"!!! Пишите количество часов цифрами, иначе бот не поймет Вас !!!",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 6
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
                sessionStorage[user_id]['last_question'] = 6
                return
            elif message == 'Snowylqrd#1100':
                vk.messages.send(user_id=user_id,
                                 message=f"Не обманывайте меня👿\n"
                                         f"Введите свой реальный никнейм в дискорде",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 5
                return
            else:
                vk.messages.send(user_id=user_id,
                                 message=f"Не обманывайте меня👿\n"
                                         f"Введите свой реальный никнейм в дискорде",
                                 random_id=rndm)
                sessionStorage[user_id]['last_question'] = 5
                return

        if quests == 6:
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
                sessionStorage[user_id]['last_question'] = 7
                return

        if quests == 7:
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
            sessionStorage[user_id]['last_question'] = 8
            return

        if quests == 8:
            vk.messages.send(user_id=user_id,
                             message=f"Поздравляем!🥳\n Ваша заявка была отправлена на рассмотрение "
                                     f"администрации клана.\n"
                                     f"⚠ Примерное время ожидания составляет ~ 1 день",
                             random_id=rndm)

            vk.messages.send(user_id=570864703,
                             message=f"У вас новая заявка от @id{user_id}",
                             random_id=rndm)

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
