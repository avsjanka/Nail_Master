import hashlib
import os
import logging
import time
import re
import psycopg2
from psycopg2.extras import DictCursor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from dependencies import Database
Database().create_tables()
load_dotenv()
TOKEN = '5849477649:AAFtRMPlLTzK7z7S6xRfV6vwwUYIUDZgzkg'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
scheduler = AsyncIOScheduler()

database = psycopg2.connect(user=os.environ.get("POSTGRES_USER") or 'postgres',
                                           password=os.environ.get("POSTGRES_PASSWORD") or 'postgresql' or 'postgres',
                                           host=os.environ.get("POSTGRES_HOST") or '127.0.0.1',
                                           port=5432,
                                           database=os.environ.get("POSTGRES_DB") or "Nails_DB",
                                           cursor_factory=DictCursor)


# Классы состояний для авторизации
class Auth(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    logged_in = State()
    wait_for_service = State()
    wait_for_time = State()
    wait_for_day = State()


class Reg(StatesGroup):
    wait_for_username = State()
    wait_for_password = State()
    wait_for_password_2 = State()

ENTRYTEXT = """
Привет, {}, я бот, который поможет тебе записаться к мастеру ногтевого сервиса Марго.
Для того, чтобы ты мог мною пользоваться, тебе необходимо только сказать мне начать работу.
Напиши /start, для того, чтобы сделать это.
"""

HELPTEXT = """
Доступные команды:
/start - Запуск бота
/help - Вызов справки по всем командам
/login - Вход в аккаунт
/register - Регистрация аккаунта
/cancel - Отмена действий
/list - Список услуг
/my_recordings - ПРосмтор ваших записей
/recording - ЗАпись на услугу
/logout - Выход из аккаунта
"""

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("/login"))
keyboard.add(KeyboardButton("/register"))
keyboard.add(KeyboardButton("/help"))

keyboard_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add("/cancel")


keyboard_authorized = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_authorized.add(KeyboardButton("/list"))
keyboard_authorized.add(KeyboardButton("/my_recordings"))
keyboard_authorized.add(KeyboardButton("/recording"))
keyboard_authorized.add(KeyboardButton("/logout"))
keyboard_authorized.add(KeyboardButton("/help"))

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

# ---------- start ----------
@dp.message_handler(commands = ['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_username = message.from_user.username
    logging.info(f'%{time.asctime()} %{user_id=}'
                 f' {user_full_name=} {user_username=}\nmessage:"{message.text}" \n')
    await bot.send_message(user_id,
                           ENTRYTEXT.format(message.from_user.username),reply_markup=keyboard)

# ---------- help function ----------
@dp.message_handler(commands = ['help'])
async def help_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_username = message.from_user.username
    logging.info(f'{time.asctime()} {user_id=} '
                 f'{user_full_name=} {user_username=}\nmessage:"{message.text}" \n')
    await bot.send_message(user_id,
                           HELPTEXT.format(message.from_user.username))

# ---------- register of user ----------
@dp.message_handler(commands = ['register'])
async def register(message: types.Message):
    msg = await message.answer("Привет! Добро пожаловать. Для начала зарегистрируемся.",
                               reply_markup=keyboard_cancel)
    msg = await message.answer("Пожалуйста, введите ваше имя пользователя:")
    await Reg.wait_for_username.set()

@dp.message_handler(state = Reg.wait_for_username)
async def username(message: types.Message, state: FSMContext):
    login = message.text
    if message.text == '/cancel':
        await message.answer(f"Возвращение на стартовую клавиатуру", reply_markup=keyboard)
        await state.finish()
        return
    if re.match("^[a-zA-Z0-9_.-]+$", login) is None:
        msg = await message.answer("В нике обнаружены недопустимые символы. Повторите попытку.")
        await Reg.wait_for_username.set()
        return

    with database.cursor(cursor_factory = DictCursor) as is_registered:
        is_registered.execute('''
                    SELECT "id_client", "login"
                    FROM "Client"
                    WHERE "login"=%s''', (login,))
        client = is_registered.fetchone()
        database.commit()
        if client is not None:
            print(client.get('login'))
            msg = await message.answer("Это имя уже занято! Попробуйте другое.")
            await Reg.wait_for_username.set()
        else:
            await state.update_data(login=login)
            msg = await message.answer("Пожалуйста, введите ваш пароль.")
            await Reg.wait_for_password.set()

@dp.message_handler(state = Reg.wait_for_password)
async def password(message: types.Message, state: FSMContext):
    password = message.text
    if message.text == '/cancel':
        await message.answer(f"Возвращение на стартовую клавиатуру", reply_markup=keyboard)
        await state.finish()
        return
    await state.update_data(password=password)
    msg = await message.answer("Пожалуйста, повторите ваш пароль.")
    await Reg.wait_for_password_2.set()


@dp.message_handler(state = Reg.wait_for_password_2)
async def password_2(message: types.Message, state: FSMContext):
    password = message.text
    if message.text == '/cancel':
        await message.answer(f"Возвращение на стартовую клавиатуру", reply_markup=keyboard)
        await state.finish()
        return
    await state.update_data(password_2=password)
    data = await state.get_data()
    if data.get('password') == data.get('password_2'):
        try:
            with database.cursor(cursor_factory = DictCursor) as registere:
                registere.execute('''insert into "Client" 
                                ("login", "telegramm_id","password") 
                                values (%s, %s, %s)
                                returning "id_client" as id_client, "login" as login,"telegramm_id" as telegramm_id,"password" as password''',
                                (str(data.get('login')), message.from_user.id ,str(hashlib.sha256(data.get('password').encode()).hexdigest())))
                database.commit()
            msg = await message.answer(f"Поздравляю, {data.get('login')}, Вы зарегистрировались!", reply_markup=keyboard_authorized)
            await Auth.logged_in.set()
        except Exception as e:
            await message.answer(e)
            print(e)
            msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
            await state.finish()
    else:
        msg = await message.answer(f"Пароли не совпадают. Повторите попытку.")
        msg = await message.answer(f"Введите пароль.")
        await Reg.wait_for_password.set()


#----------login----------
@dp.message_handler(commands = ['login'])
async def login(message: types.Message):
    msg = await message.answer("Привет! Добро пожаловать. Вы хотите зайти в свой аккаунт?",
                               reply_markup=keyboard_cancel)
    msg = await message.answer("Пожалуйста, введите ваше имя пользователя:")
    await Auth.waiting_for_username.set()

@dp.message_handler(state = Auth.waiting_for_username)
async def username(message: types.Message, state: FSMContext):
    login = message.text
    if message.text == '/cancel':
        await message.answer(f"Возвращение на стартовую клавиатуру", reply_markup=keyboard)
        await state.finish()
        return
    if re.match("^[a-zA-Z0-9_.-]+$", login) is None:
        msg = await message.answer("В нике обнаружены недопустимые символы. Повторите попытку.")
        await Auth.waiting_for_username.set()
        return

    with database.cursor(cursor_factory = DictCursor) as is_registered:
        is_registered.execute('''
                    SELECT "id_client", "login"
                    FROM "Client"
                    WHERE "login"=%s''', (login,))
        client = is_registered.fetchone()
        database.commit()
        if client is not None:
            await state.update_data(login = login)
            msg = await message.answer(f"{login}, введите ваш пароль:")
            await Auth.waiting_for_password.set()
        else:
            msg = await message.answer("Нет пользователя с таким именем, пожалуйста зарегистрируйтесь!")
            await Auth.waiting_for_username.set()

@dp.message_handler(state = Auth.waiting_for_password)
async def username(message: types.Message, state: FSMContext):
    password = message.text
    if message.text == '/cancel':
        await message.answer(f"Возвращение на стартовую клавиатуру", reply_markup=keyboard)
        await state.finish()
        return
    data = await state.get_data()
    with database.cursor(cursor_factory = DictCursor) as is_registered:
        is_registered.execute('''
                    SELECT "id_client", "login", "password"
                    FROM "Client"
                    WHERE "login"=%s''', (str(data.get('login')),))
        client = is_registered.fetchone()
        database.commit()
    if client.get("password") == str(hashlib.sha256(password.encode()).hexdigest()):
        try:
            with database.cursor(cursor_factory = DictCursor) as registere:
                registere.execute('''update "Client" set telegramm_id = %s where login = %s''',
                ( message.from_user.id, str(data.get('login'))))
                database.commit()
            msg = await message.answer(f"Поздравляю, {data.get('login')}, Вы авторизовались!", reply_markup=keyboard_authorized)
            await Auth.logged_in.set()
        except Exception as e:
            await message.answer(e)
            print(e)
            msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
            await state.finish()

#----------recording----------
@dp.message_handler(commands = ['recording'],  state = Auth.logged_in)
async def recording(message: types.Message, state: FSMContext):
    msg = await message.answer("Привет! Добро пожаловать. Вы хотите записаться на услугу?",
                               reply_markup=keyboard_cancel)
    data = await state.get_data()
    try:
            with database.cursor(cursor_factory = DictCursor) as show_services:
                show_services.execute('''SELECT * FROM "Service"''')
                services = show_services.fetchall()
                database.commit()
                str = "Список услуг:\n\n"
                buttons_new = []
                for i in range(0,len(services)):
                    str = str + f'''№{services[i].get('id_service')} {services[i].get('name_service')} - {services[i].get('price')}\n'''
                    buttons_new.append(services[i].get('id_service'))
            msg = await message.answer(str)
            msg = await message.answer(
                    text = f"{data.get('login')}, введите номер услуги, на которую хотите записаться:",
                    reply_markup = make_row_keyboard(buttons_new)
            )
            await Auth.wait_for_service.set()
            return
    except Exception as e:
        await message.answer(e)
        print(e)
        msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
        await state.finish()
        return

@dp.message_handler(state = Auth.wait_for_service)
async def set_service(message: types.Message,state: FSMContext):
    service = message.text
    data = await state.get_data()
    if re.match("^[0-9]+$", service) is None:
         msg = await message.answer(f"{data.get('login')}, вы ввели не номер услуги")
         await Auth.wait_for_service.set()
         return
    else:
        try:
            with database.cursor(cursor_factory = DictCursor) as show_services:
                show_services.execute('''SELECT * FROM "Service" where "id_service" = %s''',(int(service),))
                services = show_services.fetchall()
                database.commit()
            if services is not None:
                await state.update_data( service = service)
                with database.cursor(cursor_factory = DictCursor) as is_not_recorded:
                    is_not_recorded.execute('''
                                SELECT *
                                FROM "Dates_for_recordings"
                                WHERE "is_recorded"= false''')
                    day_for_rec =  is_not_recorded.fetchall()
                    database.commit()
                    str = f"{data.get('login')}, выберете  дату получения услуги из предложенных:\nгг-мм-дд\n"
                    for i in range(0,len(day_for_rec)):
                        str = str + f'''{day_for_rec[i].get('date_str')} - {day_for_rec[i].get('time')}:00\n'''
                msg = await message.answer(str)
                await Auth.wait_for_day.set()
                return
            else:
                 msg = await message.answer(f"{data.get('login')}, вы ввели несуществующий номер услуги:")
                 await Auth.wait_for_service.set()
        except Exception as e:
            await message.answer(e)
            print(e)
            msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
            await state.finish()
            return

@dp.message_handler(state = Auth.wait_for_day)
async def set_service(message: types.Message,state: FSMContext):
    day = message.text
    data = await state.get_data()
    if re.match("^[0-9-]+$", day) is None:
         msg = await message.answer(f"{data.get('login')}, вы ввели не дату.")
         await Auth.wait_for_day.set()
         return
    else:
        try:
            with database.cursor(cursor_factory = DictCursor) as is_not_recorded:
                    is_not_recorded.execute('''
                                SELECT *
                                FROM "Dates_for_recordings"
                                WHERE "is_recorded"= false and "date_str" = %s''',(day,))
                    days_for_recording = is_not_recorded.fetchall()
                    database.commit()
            if days_for_recording is not None:
                await state.update_data( day = day)
                with database.cursor(cursor_factory = DictCursor) as is_not_recorded:
                    is_not_recorded.execute('''
                                SELECT *
                                FROM "Dates_for_recordings"
                                WHERE date_str = %s and is_recorded = false ''',(day,))
                    time_for_rec = is_not_recorded.fetchall()
                    database.commit()
                    str = f"{data.get('login')}, выберете  время получения услуги из предложенных в эту дату {day}:\n"
                    buttons_new = []
                    for i in range(0,len(time_for_rec)):
                        str = str + f'''{time_for_rec[i].get('time')}:00\n'''
                        buttons_new.append(time_for_rec[i].get('time'))
                msg = await message.answer(str)
                msg = await message.answer(
                    text = f"{data.get('login')}, введите время услуги, на которое вы хотите записаться:",
                    reply_markup = make_row_keyboard(buttons_new)
                )
                await Auth.wait_for_time.set()
                return
            else:
                msg = await message.answer(f"{data.get('login')}, вы ввели несуществующую дату.")
                await Auth.wait_for_day.set()
                return

        except Exception as e:
            await message.answer(e)
            print(e)
            msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
            await state.finish()
            return


@dp.message_handler(state = Auth.wait_for_time)
async def set_service(message: types.Message, state: FSMContext):
    time = message.text
    data = await state.get_data()
    if re.match("^[0-9]+$", time) is None:
         msg = await message.answer(f"{data.get('login')}, вы ввели не время")
         await Auth.wait_for_service.set()
         return
    else:
        try:
            with database.cursor(cursor_factory = DictCursor) as is_not_recorded:
                    is_not_recorded.execute('''
                                SELECT *
                                FROM "Dates_for_recordings"
                                WHERE "is_recorded"= false and "time" = %s''',(time,))
                    time_for_recording = is_not_recorded.fetchall()
                    database.commit()
            if time_for_recording is not None:
                with database.cursor(cursor_factory = DictCursor) as is_registered:
                    is_registered.execute('''
                        SELECT "id_client", "login"
                        FROM "Client"
                        WHERE "login"=%s''', (data.get('login'),))
                    result = is_registered.fetchone()
                    database.commit()
                id = result.get('id_client')
                with database.cursor(cursor_factory = DictCursor) as cursor:
                         cursor.execute('''insert into "Data" 
                                                    ("data", "time") 
                                                    values (%s, %s)
                                                    returning "id_time" as id_time, "data" as data, "time" as time''', (data.get('day'), int(time)))
                         data_rec = cursor.fetchone()
                         database.commit()
                date = data_rec.get('id_time')
                with database.cursor(cursor_factory = DictCursor) as cursor:
                            cursor.execute('''insert into "Recording"
                                                        ("id_client","id_time","service")
                                                        values(%s,%s,%s) 
                                                        returning "id_rec" as id_rec,"id_client" as id_client,"id_time" as id_time,"service" as service''',
                                           (id,date,int(data.get('service'))))
                            database.commit()
                with  database.cursor(cursor_factory = DictCursor) as cursor:
                    cursor.execute('''update "Dates_for_recordings" set "is_recorded"= true
                                      where date_str = %s and "time" = %s''',
                                           (data.get('day'), int(time)))
                    database.commit()
                msg = await message.answer(f"{data.get('login')}, вы успешно записались на услугу №{data.get('service')} {data.get('day')} в {time}:00.",
                                           reply_markup=keyboard_authorized)
                await Auth.logged_in.set()
                return
            else:
                msg = await message.answer(f"{data.get('login')}, вы ввели несуществующее время.")
                await Auth.wait_for_time.set()
                return

        except Exception as e:
            await message.answer(e)
            print(e)
            msg = await message.answer(f"Что-то пошло не так, {data.get('login')}, обратитесь к администратору.")
            await state.finish()
            return


#----------list----------
@dp.message_handler(commands = ['list'],  state = Auth.logged_in)
async def list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    with database.cursor(cursor_factory = DictCursor) as show_services:
                show_services.execute('''SELECT * FROM "Service"''')
                services = show_services.fetchall()
                database.commit()
    str = "Список услуг:\n\n"
    buttons_new = []
    for i in range(0,len(services)):
        str = str + f'''№{services[i].get('id_service')} {services[i].get('name_service')} - {services[i].get('price')}\n'''
        buttons_new.append(services[i].get('id_service'))
    msg = await message.answer(str)
    await Auth.logged_in.set()
    return


#----------my_recordings----------
@dp.message_handler(commands=["my_recordings"], state = Auth.logged_in)
async def my_recs(message: types.Message, state: FSMContext):
    data = await state.get_data()
    with database.cursor(cursor_factory = DictCursor) as login:
        login.execute('''
                    SELECT "id_client", "login"
                    FROM "Client"
                    WHERE "login"=%s''', (data.get('login'),))
        client = login.fetchone()
        database.commit()
    id = client.get('id_client')
    with database.cursor(cursor_factory = DictCursor) as recordings:
         recordings.execute('''select * from "Recording" join "Service" ON service = id_service
                                 join "Data" on "Recording".id_time = "Data".id_time
                                 where id_client = %s''', (id,))
         list_recordings = recordings.fetchall()
    str = f"{data.get('login')}, вы записаны на:\n"
    for i in range(0,len(list_recordings)):
        str = str + f"{list_recordings[i].get('name_service')} {list_recordings[i].get('data')} в {list_recordings[i].get('time')}:00\n"
    msg = await message.answer(str)
    await Auth.logged_in.set()
    return


#----------logout---------
@dp.message_handler(commands="logout", state=Auth.logged_in)
async def user_logout(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f"Вы вышли из аккаунта{data.get('login')}.", reply_markup=keyboard)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)
