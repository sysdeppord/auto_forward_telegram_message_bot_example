ver_app =  "v 0.0.2.5 nightly"
name_app = "Forward bot by: @SYSdeppord "
device_model = "SYSdeppord govno cloud"
system_version = "Linux chroot on Android"
print(name_app + ver_app + " \nИмпорт библиотек")

import sqlite3
from pyrogram import Client, filters


# Config functions
config_file = 'setting.db'
my_id = 0
my_setting = ()
forward_setting = []
user_list_info = []
f_self = 0

cmd = "`/help` - Показывает справку по командам (данное сообщение)\n" \
      "`/info` - Информация о версии бота\n" \
      "`/start` - __Снимает бота с паузы (не влияет на отдельные аккаунты, в которых пересылка на паузе)__\n" \
      "`/stop` - Ставит бота на паузу (доступны только настройки)\n" \
      "`/setting` - Вход в режим настройки бота\n" \
      "`/exit` - Выход из режима настройки бота\n" \
      "`/add` - Добавление контакта в список пересылки\n" \
      "`/remove` - Удаляет контакт из списка пересылки (канал куда пересылались сообщения не удаляется)\n" \
      "`/list` - Показыват список пересылок сообщений, от кого и куда\n" \
      "`/freeze` - Замораживает пересылку от конкретного контакта\n" \
      "`/unfreeze` - Восстанавливает замороженую пересылку от конкретного контакта\n" \
      "`/forward_my` - Вкл/Выкл пересылку собственных (исходящих от себя) сообщений\n\n" \
      "`/burn_all` - **ВАЙП К ХУЯМ ВСЕХ КАНАЛОВ КУДА ПЕРЕСЫЛАЮТСЯ СООБЩЕНИЯ И ИХ УДАЛЕНИЕ, А ТАКЖЕ УДАЛЯЕТ" \
      " ВСЕ НАСТРОЙКИ ПЕРЕСЫЛОК И СТОПАЕТ БОТА НАХУЙ!!!\nВОССТАНОВЛЕНИЕ НЕВОЗМОЖНО!!! ПОСЛЕ ЭТОГО БОТ БЛОКИРУЕТСЯ!!!" \
      " ТЫ НЕ СМОЖЕШЬ ЮЗАТЬ В БОТЕ НИ-ЧЕ-ГО\nРазблокировка бота по твоему аккаунту только у @sysdeppord !!!" \
      " ПЛАТНАЯ!!! АНАЛОМ СУКА!!!**"

class cfg:

    def load(): # loading config file
        global my_setting
        global forward_setting
        print("Loading config")
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='my_setting'")
        if cur.fetchone()[0] == 1:
            print('Table "my_setting" exists.')
        else:
            print('Table "my_setting" does not exist, creating...')
            cur.execute("CREATE TABLE my_setting(user, pause, license_accept, premium)")
            data = [(0, 0, 0, 0)]
            cur.executemany("INSERT INTO my_setting VALUES(?, ?, ?, ?)", data)
            print("OK")
        for row in cur.execute("SELECT user, pause, license_accept, premium FROM my_setting ORDER BY user"):
            my_setting = row
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='forward_setting'")
        if cur.fetchone()[0] == 1:
            print('Table "forward_setting" exists.')
        else:
            print('Table "forward_setting" does not exist, creating...')
            cur.execute("CREATE TABLE forward_setting(user, forward_to, enable, forward_self, mark_as_read)")
            print("OK")
        for row in cur.execute("SELECT user, forward_to, enable, forward_self, mark_as_read FROM forward_setting ORDER BY user"):
            forward_setting.append(list(row))
        con.commit()
        con.close()
        print("Config loaded!")

    def forward_update(): # Need for update configs forwarding
        global forward_setting
        forward_setting.clear()
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        for row in cur.execute("SELECT user, forward_to, enable, forward_self, mark_as_read FROM forward_setting ORDER BY user"):
            forward_setting.append(row)
        con.commit()
        con.close()
        print("Forward config updated!")
        return "OK"

    def add_to_forwarding(user_id, forward_to): # Adding parameters user/chat|group|channel
        user = user_id
        to = forward_to
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        data = [(user, to, 1, 1, 0)]
        cur.executemany("INSERT INTO forward_setting VALUES(?, ?, ?, ?, ?)", data)
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"

    def forward_contact_enable(user_id, status): # Adding parameters user|enable forwarding from chat
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "UPDATE forward_setting SET enable = " + str(status) + " WHERE user = " + str(user_id)
        cur.execute(sql)
        print("Forwarding removed!")
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"

    def pause(status): # Select pause status of all forwarding (bot run/pause forwarding)
        status = status
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "UPDATE my_setting SET pause = "+ str(status) +" WHERE user = 0"
        cur.execute(sql)
        print("Global setting forwarding canged and updated!")
        con.commit()
        con.close()
        cfg.main_setting_update()
        return "OK"

    def main_setting_update(): # Updating main setting
        global my_setting
        global pause
        temp_my_setting = list(my_setting)
        temp_my_setting.clear()
        my_setting = tuple(temp_my_setting)
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        for row in cur.execute(
                "SELECT user, pause, license_accept, premium FROM my_setting ORDER BY user"):
            my_setting = row
            print(row)
        con.commit()
        con.close()
        pause = my_setting[1]
        print("MAIN config updated!")

        return "OK"

    def forward_self(user_id, status): # Select status of forwarding self messages
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "UPDATE forward_setting SET forward_self = " + str(status) + " WHERE user = " + str(user_id)
        cur.execute(sql)
        print("Forwarding self status changed!")
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"
# future
    def mark_as_read(user_id, status): # Select status of marking forwarded messages as read
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "UPDATE forward_setting SET mark_as_read = " + str(status) + " WHERE user = " + str(user_id)
        cur.execute(sql)
        print("Forwarding self status changed!")
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"

    def del_forward(user): # Deleting forward info
        user = user
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "DELETE FROM forward_setting WHERE user = " + str(user)
        cur.execute(sql)
        print("Forwarding removed!")
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"
# Future
    def license_accept(status):
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "UPDATE my_setting SET license_accept = '" + str(status) + "' WHERE user = 'user'"
        cur.execute(sql)
        print("License accepted")
        con.commit()
        con.close()
        cfg.main_setting_update()
        return "OK"

    def del_all_forwardings():
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "DELETE FROM forward_setting"
        cur.execute(sql)
        print("FORWARD SETTING WIPED!!!!")
        con.commit()
        con.close()
        cfg.forward_update()
        return "OK"


cfg.load()


def forward_logic(user_chat_id):
    global forward_setting
    user_id = user_chat_id
    for item in forward_setting:
        if item[0] == user_id:
            fs = [item[1], item[2], item[3]]
            return fs
        else:
            return False

async def user_info(user_id):
    user_id = user_id
    user = await app.get_users(user_id)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    is_contact = user.is_contact
    return "пользователя \"" + first_name + "\" (@" + username + "\") "

async def channel_info(channel_id):
    channel_id = channel_id
    channel_info = await app.get_chat(channel_id)
    channel_name = channel_info.title
    return channel_name

async def user_list_build():
    global forward_setting #user, forward_to, enable, forward_self, mark_as_read
    global user_list_info
    user_list_info.clear()
    id = 0
    for user in forward_setting:
        main = await user_info(user[0])
        uID = user[0]
        forward_to = await channel_info(user[1])
        enable = user[2]
        forward_self = user[3]
        line = [id, uID, main, forward_to, enable, forward_self]
        user_list_info.append(line)
    return user_list_info

async def burn_all():
    global forward_setting #user, forward_to, enable, forward_self, mark_as_read
    for user in forward_setting:
        delete_channel = user[1]
        await app.delete_channel(delete_channel)
    cfg.del_all_forwardings()


pause = my_setting[1]
api_id = 00000000
api_hash = "xxxxxxxxxxxxxxxxxxxxxx"
app = Client("test000", api_id=api_id, api_hash=api_hash, app_version=name_app+ver_app, device_model=device_model,
             system_version=system_version)

setting_mode = 0
menu_point = 0

class setting_logic:


    def start():
        return "Ты запустил настройку автоматической пересылки сообщений!\nНапиши `/exit` для выхода из режима " \
               "настройки.\nОтправь `/help` для вывода списка всех комманд."

    def exit():
        global menu_point
        global setting_mode
        menu_point = 0
        setting_mode = 0
        return "Настройка завершена! Ты вышел из режима настройки!"

    async def message(message):
        text = message.text
        global menu_point
        global my_setting
        global forward_setting
        global pause
        global user_list_info
        global f_self
        if message.text == "/remove":
            if forward_setting == []:
                await message.edit_text(f"`{message.text}`\n\nСписок пользователей на пересылку пуст!")
            else:
                info = await user_list_build() # id, uID, main, forward_to, enable
                reply = ""
                for item in info:
                    one = str(item[0]) + " - Сообщения от " + item[2] + "пересылаются в канал \"" + item[3] + "\"," \
                                         " пересылка - " + str(item[4]) + " (1 - активна/2 - заморожена)\n"
                    reply += one
                reply = "Отправь номер из списка для удаления пользователя.\n\n"+ reply +"\n\nВажно! Нумирация идёт с нуля!"
                await message.edit_text(f"`{message.text}`\n\n{reply}")#"Выбери "
                menu_point = 2

        elif message.text == "/list":
            if forward_setting == []:
                await message.edit_text(f"`{message.text}`\n\nСписок пользователей на пересылку пуст!\nТы можешь добавить их через"
                                         " комманду `/add`")
            else:
                info = await user_list_build()  # id, uID, main, forward_to
                reply = ""
                for item in info:
                    one = str("Сообщения от " + item[2] + "пересылаются в канал \"" + item[3] + "\"\n")
                    reply += one
                await message.edit_text(f"`{message.text}`\n\n{reply}")

        elif message.text == "/info":
            global ver_app
            global device_model
            global system_version
            global name_app
            info_text = name_app + " " + ver_app + "\n" + "Powered by: " + device_model + "\n\n"
            info = info_text + "Услуга предоставляется \"КАК ЕСТЬ\"! Стабильное функционирование НЕ ГАРАНТИРУЕТСЯ," \
                               "особенно с этими блядскими отключениями света..."
            await message.edit_text(f"`{message.text}`\n\n{info}")

        elif message.text == "/freeze":
            if forward_setting == []:
                await message.edit_text(f"`{message.text}`\n\nУ тебя нет настроеных пересылок сообщений!\nИспользуй комманду `/add`"
                                         " для добавления!")
            else:
                info = await user_list_build()  # id, uID, main, forward_to
                reply = ""
                for item in info:
                    if item[4] == 1:
                        one = str(item[0]) + " - Заморозить пересылку  от " + item[2] + "\n"
                        reply += one
                if reply == "":
                    reply = "Нет доступных пользователей на заморозку пересылки сообщений!"
                await message.edit_text(f"`{message.text}`\n\n{reply}")
                if reply == "Нет доступных пользователей на заморозку пересылки сообщений!":
                    menu_point = 0
                else:
                    menu_point = 3

        elif message.text == "/unfreeze":
            if forward_setting == []:
                await message.reply_text(f"`{message.text}`\n\nУ тебя нет настроеных пересылок сообщений!\nИспользуй "
                                         "комманду `/add` для добавления!")
            else:
                info = await user_list_build()  # id, uID, main, forward_to
                reply = ""
                for item in info:
                    if item[4] == 0:
                        one = str(item[0]) + " - Разморозить пересылку  от " + item[2] + "\n"
                        reply += one
                if reply == "":
                    reply = "Нет доступных пользователей на разморозку пересылки сообщений!"
                await message.edit_text(f"`{message.text}`\n\n{reply}")
                if reply == "Нет доступных пользователей на разморозку пересылки сообщений!":
                    menu_point = 0
                else:
                    menu_point = 4

        elif message.text == "/burn_all":
            if forward_setting != []:
                await message.edit_text(f"`{message.text}`\n\nПизда тебе досточка ёбаная\nИницыирую удаление всех "
                                        "аккаунтов и вайп каналов с пересылкой.\nТы точно уверен(а), что хочешь всё "
                                        "вайпнуть К ХУЯМ?!\nЭТО ДЕЙСТВИЕ НЕ ОБРАТИМО!!!\nНапиши ответ \"ДА\" или"
                                        " \"НЕТ\"")
                menu_point = 5
            else:
                await message.edit_text(f"`{message.text}`\n\nУ тебя нет нихуя, что-бы вайпать!")

        elif message.text == "/forward_my":
            if forward_setting == []:
                await message.edit_text(f"`{message.text}`\n\nУ тебя нет настроеной пересылки, что бы настроить"
                                         " пересылку собственных сообщений!")
            else:
                info = await user_list_build() # id, uID, main, forward_to, forward_self
                reply = "Чтобы настроить действие выбери пользователя из списка:\n\n"
                for user in info:
                    one = f"{user[0]} - \"{user[2]}\". Свои сообщения пересылаются? - Status {user[5]} (0 - НЕТ/1 - ДА)\n"
                    reply += one
                reply += "\nВыбери число перед пользователем, чтобы настроить!\n--/exit-- - для выхода"
                await message.edit_text(f"`{message.text}`\n\n{reply}")
                menu_point = 6

        elif menu_point ==  6:
            if message.text.isdigit():
                choise = message.text
                choise = int(choise)
                try:
                    self_forward = user_list_info[choise][5]
                except:
                    await message.edit_text(f"`{message.text}`\n\nТакого айдишника не существует! Отправь правильный номер!")
                else:
                    f_self = user_list_info[choise][1]
                    if self_forward == 1:
                        await message.edit_text(f"`{message.text}`\n\nПересылка собственных сообщений АКТИВНА.\nДля"
                                                " деактивации отправь: **Выключить**")
                        menu_point = 7
                    elif self_forward == 0:
                        await message.edit_text(f"`{message.text}`\n\nПересылка собственных сообщений НЕ АКТИВНА.\nДля"
                                                " активации отправь: **Включить**")
                        menu_point = 7
            else:
                await message.edit_text(f"`{message.text}`\n\nОтправь цифру!\n`/exit` - для выхода")

        elif menu_point == 7:
            response = message.text
            response = response.lower()
            if response == "выключить":
                cfg.forward_self(f_self, 0)
                await message.edit_text(f"`{message.text}`\n\nПересылка собственных сообщений **ДЕАКТИВИРОВАНА**!")
                menu_point = 0
            elif response == "включить":
                cfg.forward_self(f_self, 1)
                await message.edit_text(f"`{message.text}`\n\nПересылка собственных сообщений **АКТИВИРОВАНА**!")
                menu_point = 0
            else:
                await message.edit_text(f"`{message.text}`\n\nОтправь нормально!\n`/exit` - для выхода")

        if menu_point == 5:
            global setting_mode
            text = message.text.lower()
            if text == "да":
                await message.edit_text(f"`{message.text}`\n\nНачинаю вайпать к хуям все каналы и базу")
                await burn_all()
                await message.edit_text(f"`{message.text}`\n\nВайп закончился, покеда!")
                menu_point = 0
                setting_mode = 0
            elif text == "нет":
                await message.edit_text(f"`{message.text}`\n\nНу и пошёл бы ты нахуй!\nХуле беспокоишь по пустякам?")
                menu_point = 0

        elif menu_point == 3:
            if message.text.isdigit():
                iff = int(message.text)
                try:
                    user_id_for_freeze = user_list_info[iff][1]
                except:
                    await message.edit_text(f"`{message.text}`\n\nОтправь правильный номер из списка!")
                else:
                    cfg.forward_contact_enable(user_id_for_freeze, 0)
                    menu_point = 0
                    await message.edit_text(f"`{message.text}`\n\nПересылка сообщений от пользователя была заморожена")
            else:
                await message.reply_text("Отправь номер из списка!")

        elif menu_point == 4:
            if message.text.isdigit():
                ifuf = int(message.text)
                try:
                    user_id_for_unfreeze = user_list_info[ifuf][1]
                except:
                    await message.edit_text(f"`{message.text}`\n\nОтправь правильный номер из списка!")
                else:
                    cfg.forward_contact_enable(user_id_for_unfreeze, 1)
                    menu_point = 0
                    await message.edit_text(f"`{message.text}`\n\nПересылка сообщений от пользователя была разморожена")
            else:
                await message.reply_text("Отправь номер из списка!")

        elif menu_point == 2:
            if message.text.isdigit():
                ifr = int(message.text)
                try:
                    user_id_for_remove = user_list_info[ifr][1]
                except:
                    await message.edit_text(f"`{message.text}`\n\nТакого айдишника не существует! Отправь правильный номер!")
                else:
                    cfg.del_forward(user_id_for_remove)
                    await message.edit_text(f"`{message.text}`\n\nПользователь {user_list_info[ifr][2]} был удалён из"
                                            f" системы пересылки сообщений.\nКанал {user_list_info[ifr][3]} для"
                                            " пересылки сообщений остался не тронут.")
                    menu_point = 0
            else:
                await message.reply_text(f"`{message.text}`\n\nОтправь номер из списка!")

        elif message.text == "/add":
            if menu_point == 0:
                menu_point = 1
                await message.edit_text(f"`{message.text}`\n\nПерешли СЮДА контакт пользователя, от которого нужно "
                                        "автоматически пересылать сообщения. Канал создастся автоматически.\nВАЖНО!!! "
                                        "Пока пользователя можно добавить только через пересылку контакта!!!")
        elif menu_point == 1:
            try:
                message.contact.user_id > 0
            except:
                await message.edit_text(f"`{message.text}`\n\nТы отправил не контакт, попробуй ещё раз.")
            else:
                from_id = message.contact.user_id
                in_list = forward_logic(from_id)
                if in_list == None:
                    channel_name = message.contact.first_name + " Сохранённые сообщения (id " + str(
                        message.contact.user_id) + ")"
                    create_channel = await app.create_channel(channel_name, "Не удаляй, если используется пересылка, "
                                                                            "иначе бот упадёт при пересылке сообщений "
                                                                            "от этого юзера")
                    forward = create_channel.id
                    cfg.add_to_forwarding(from_id, forward)
                    menu_point = 0
                    await message.reply_text(f"Канал куда пересылаются сообщения создан "
                                            f"**\"{channel_name}\"**!\nТеперь ты можешь его переименовать по своему"
                                            f" желанию!\nВАЖНО!!!\nНе удаляй канал, для пересылки сообщений, иначе бот"
                                            " пошлёт тебя нахуй!")
                else:
                    await message.edit_text(f"`{message.text}`\n\nЭтот ползователь уже есть в списке на пересылку!")


@app.on_message(filters.command(["start"]) & filters.me)
async def command_start(client, message):
    global pause
    if pause == 0:
        print("status pause is: " + str(pause))
        await message.edit_text(f"`{message.text}`\n\nБот уже запущен!\nОтправь `/stop` для остановки.\nОбратись к @SYSdeppord для "
                                 "информации, если что-то пошло не так и сообщения не пересылаются.")
    else:
        print("status pause is: " + str(pause))
        status = 0
        cfg.pause(status)
        await message.edit_text(f"`{message.text}`\n\nБот запущен!\nДля остановки отправь `/stop`")

@app.on_message(filters.command(["stop"]) & filters.me)
async def command_stop(client, message):
    global pause
    if pause == 1:
        print("status pause is: " + str(pause))
        await message.reply_text(f"`{message.text}`\n\nБот уже остановлен!\nОтправь /start для запуска.\nОбратись к @SYSdeppord для "
                                 "информации, если что-то пошло не так и сообщения продолжают пересілаться.")
    else:
        status = 1
        cfg.pause(status)
        print("status pause is: "+str(pause))
        await message.reply_text(f"`{message.text}`\n\nБот остановлен!\nДля повторного запуска отправь /start")

@app.on_message(filters.private & filters.text)
async def text_message(client, message):
    global setting_mode
    global my_id
    global pause
    global forward_setting
    global cmd
    if my_id == 0:
        me = await app.get_me()
        my_id = me.id
    if message.chat.id == my_id:
        if message.text == "/setting":
            setting_mode = 1
            await message.edit_text(f"`{message.text}`\n\n{setting_logic.start()}")
        elif message.text == "/exit":
            await message.edit_text(f"`{message.text}`\n\n{setting_logic.exit()}")
        elif message.text == "/help":
            await message.edit_text(f"`{message.text}`\n\n {cmd}")
        else:
            if setting_mode == 1:
                await setting_logic.message(message)
            else:
                pass
    else:
        ft = forward_logic(message.chat.id)
        if ft:
            forward_to = ft[0]
            enable = ft[1]
            forward_self = ft[2]
            usr_id = message.from_user.id
            if pause == 0:
                if enable == 1:
                    if usr_id == my_id:
                        if forward_self:
                            await message.forward(forward_to)
                    else:
                        await message.forward(forward_to)

@app.on_message(filters.private & filters.video)
async def forward_videos(client, message):
    global pause
    ft = forward_logic(message.chat.id)
    if ft:
        forward_to = ft[0]
        enable = ft[1]
        forward_self = ft[2]
        usr_id = message.from_user.id
        if pause == 0:
            if enable == 1:
                if usr_id == my_id:
                    if forward_self:
                        try:
                            message.video.ttl_seconds > 0
                        except TypeError:
                            await message.forward(forward_to)
                        else:
                            print("Protected video! DOWNLOADING...")
                            print("Burnning delay - " + str(message.video.ttl_seconds))
                            async def progress(current, total):
                                print(f"{current * 100 / total:.1f}%")
                            await app.download_media(message)
                            file_caption = "Сгораемое ВИДЕО от пользователя \""+ message.from_user.first_name +\
                                           "\", дата и время сообщения \""+str(message.date)+"\""
                            await app.send_document(forward_to, await app.download_media(message, in_memory=True),
                                                    force_document=True, caption=file_caption, progress=progress)
                else:
                    try:
                        message.video.ttl_seconds > 0
                    except TypeError:
                        await message.forward(forward_to)
                    else:
                        print("Protected video! DOWNLOADING...")
                        print("Burnning delay - " + str(message.video.ttl_seconds))

                        async def progress(current, total):
                            print(f"{current * 100 / total:.1f}%")

                        await app.download_media(message)
                        file_caption = "Сгораемое ВИДЕО от пользователя \"" + message.from_user.first_name + \
                                       "\", дата и время сообщения \"" + str(message.date) + "\""
                        await app.send_document(forward_to, await app.download_media(message, in_memory=True),
                                                force_document=True, caption=file_caption, progress=progress)


@app.on_message(filters.private & filters.photo)
async def forward_photos(client, message):
    global pause
    ft = forward_logic(message.chat.id)
    if ft:
        forward_to = ft[0]
        enable = ft[1]
        forward_self = ft[2]
        usr_id = message.from_user.id
        if pause == 0:
            # if forward_to != None: MB delete???
            if enable == 1:
                    if usr_id == my_id:
                        if forward_self:
                            try:
                                message.photo.ttl_seconds > 0
                            except TypeError:
                                await message.forward(forward_to)
                            else:
                                print("Is protected!!!\nDOWNLOADING...")
                                print("Burned delay - " + str(message.photo.ttl_seconds))

                                async def progress(current, total):
                                    print(f"{current * 100 / total:.1f}%")

                                await app.download_media(message)
                                file_caption = "Сгораемое ФОТО от пользователя \"" + message.from_user.first_name + \
                                               "\", дата и время сообщения \"" + str(message.date) + "\""
                                await app.send_document(forward_to, await app.download_media(message, in_memory=True),
                                                        force_document=True, caption=file_caption, progress=progress)

                    else:
                        try:
                            message.photo.ttl_seconds > 0
                        except TypeError:
                            await message.forward(forward_to)
                        else:
                            print("Is protected!!!\nDOWNLOADING...")
                            print("Burned delay - " + str(message.photo.ttl_seconds))
                            async def progress(current, total):
                                print(f"{current * 100 / total:.1f}%")
                            await app.download_media(message)
                            file_caption = "Сгораемое ФОТО от пользователя \"" + message.from_user.first_name + \
                                           "\", дата и время сообщения \"" + str(message.date) + "\""
                            await app.send_document(forward_to, await app.download_media(message, in_memory=True),
                                                    force_document=True, caption=file_caption, progress = progress)

@app.on_message(filters.private & ~filters.text & ~filters.video & ~filters.photo)
async def forward_other_media(client, message):
    global pause
    if message.chat.id == my_id:# and setting_mode:
        await setting_logic.message(message)
    else:
        ft = forward_logic(message.chat.id)
        if ft:
            forward_to = ft[0]
            enable = ft[1]
            forward_self = ft[2]
            usr_id = message.from_user.id
            if pause == 0:
                # if forward_to != None: - MB delete???
                if enable == 1:
                    if usr_id == my_id:
                        if forward_self:
                            await message.forward(forward_to)
                    else:
                        await message.forward(forward_to)

@app.on_message(filters.private & filters.media_group)
async def forward_media_group(client, message):
    global pause
    ft = forward_logic(message.chat.id)
    if ft:
        forward_to = ft[0]
        enable = ft[1]
        forward_self = ft[2]
        usr_id = message.from_user.id
        if pause == 0:
            # if forward_to != None: - MB delete???
            if enable == 1:
                if usr_id == my_id:
                    if forward_self:
                        await message.forward(forward_to)
                else:
                    await message.forward(forward_to)

print("All setting loaded!")
print("Подключение к телеграм аккаунту")
app.run()
