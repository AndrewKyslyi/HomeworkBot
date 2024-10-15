from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from dotenv import load_dotenv

import os
import buttons
import datetime
import sqlite3
import asyncio
import random

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


class Form(StatesGroup):
    user_data = State()
    al_homework = State()
    ge_homework = State()
    ch_homework = State()
    ph_homework = State()
    en_homework = State()
    uk_homework = State()
    fr_homework = State()


# Создание бд и таблиц || Create bd and tables
def create_db():
    conn = sqlite3.connect('UsersData.sql')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, 
        number_of_class INTEGER, letter_of_class TEXT, user_name TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS dz (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT UNIQUE, 
        homework TEXT, today TEXT)""")
    conn.commit()
    conn.close()


create_db()


@dp.message(Command("start"))
async def handle_start(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Привіт пупсик😏😏! Цей бот створений для зручного пошуку та записування домашнього "
                             "завдання! \nАле перед усім потрібно виконати декілька кроків"
                             "\nНапиши <i><b>/reg</b></i> для того щоб продовжити", parse_mode='HTML')


# Start to log in user after command: /next
@dp.message(Command("reg"))
async def next_step(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        conn = sqlite3.connect("UsersData.sql")
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM members""")
        user_name = cursor.fetchall()
        conn.commit()
        conn.close()
        if message.from_user.username not in str(user_name):
            await message.answer("Окей! Далі напиши в такій послідовності своє ім'я, прізвище, рік навчання, "
                                 "літеру класу.\n(Через пробіл: iм'я прiзвище рiк лiтера)")
            await state.set_state(Form.user_data)
        else:
            await message.answer("Ви вже зареєстровані!")
            return


@dp.message(Form.user_data)
async def write_data(message: types.Message, state: FSMContext):
    conn = sqlite3.connect("UsersData.sql")
    cursor = conn.cursor()
    cursor.execute("""SELECT user_name FROM members""")
    user_name = cursor.fetchall()
    conn.commit()
    conn.close()
    user_data = message.text.split(' ') or message.text.split(',')
    await state.update_data(user_data=user_data)
    if message.chat.type == 'private':
        if message.from_user.username not in user_name:
            conn = sqlite3.connect('UsersData.sql')
            cursor = conn.cursor()
            cursor.execute("""INSERT OR IGNORE INTO members (name, surname, number_of_class, 
                                                                      letter_of_class, user_name) VALUES (?, ?, ?, ?, ?)""",
                           (user_data[0], user_data[1], user_data[2], user_data[3], message.from_user.username))
            conn.commit()

            await message.answer(
                "Тепер ви у системі, вітаю😁👍!! \nМожете обрати предмет та додати або взнати домашнє завдання",
                reply_markup=buttons.subjects)
            await state.clear()
        else:
            return
        conn.commit()
        conn.close()


# Start to add subject
@dp.message(Command("homework"))
async def add_subject(message: types.Message):
    if message.chat.type == 'private':
        await message.answer("Ось доступні предмети\nМожете обрати предмет та записати або дізнатися домашнє завдання",
                             reply_markup=buttons.subjects)


@dp.callback_query(lambda x: x.data == 'algebra' or x.data == 'geometry' or x.data == 'chemistry' or x.data == 'physics' or x.data == 'english' or x.data == 'ukrainian' or x.data == 'french')
async def decor(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        await call.message.answer('Люблю Максимчика<3<3<3😍❤️💕😍💕😘😍💕')


# On Inline Button "Алгебра"
@dp.callback_query(lambda x: x.data == 'al_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect("UsersData.sql")
    cursor = conn.cursor()
    cursor.execute("""SELECT user_name FROM members""")
    user_name = cursor.fetchall()
    conn.commit()
    conn.close()
    if call.message.chat.type == 'private':
        if call.from_user.username in str(user_name):
            await call.message.answer('Добре, запишемо домашнє завдання з алгебри!\nНапиши сюди завдання')
            await state.set_state(Form.al_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.al_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    await state.update_data(al_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('Algebra',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'Algebra'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з алгебри було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'al_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('Algebra',))
        homework = cursor.fetchall()
        print(homework)
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з алгебри:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}',
                parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з алгебри поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'gm_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect("UsersData.sql")
    cursor = conn.cursor()
    cursor.execute("""SELECT user_name FROM members""")
    user_name = cursor.fetchall()
    conn.commit()
    conn.close()
    if call.message.chat.type == 'private':
        if call.from_user.username in str(user_name):
            await call.message.answer('Файно, запишемо домашнє завдання з геометрії!\nНапиши сюди завдання')
            await state.set_state(Form.ge_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.ge_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])
    await state.update_data(ge_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('Geometry',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'Geometry'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з геометрії було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'gm_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('Geometry',))
        homework = cursor.fetchall()
        print(homework)
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з геометрії:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}',
                parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з геометрії поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'ch_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect("UsersData.sql")
    cursor = conn.cursor()
    cursor.execute("""SELECT user_name FROM members""")
    user_name = cursor.fetchall()
    conn.commit()
    conn.close()
    if call.message.chat.type == 'private':
        if call.from_user.username in str(user_name):
            await call.message.answer('Жах, запишемо домашнє завдання з хімії!\nНапиши сюди завдання')
            await state.set_state(Form.ch_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.ch_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    print(date)
    await state.update_data(ch_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('Chemistry',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'Chemistry'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з хімії було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'ch_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('Chemistry',))
        homework = cursor.fetchall()
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з хімії:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}', parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з хімії поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'ph_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect("UsersData.sql")
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM members""")
        user_name = cursor.fetchall()
        conn.commit()
        conn.close()
        if call.from_user.username in str(user_name):
            await call.message.answer('Добре, запишемо домашнє завдання з фізики!\nНапиши сюди завдання')
            await state.set_state(Form.ph_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.ph_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    print(date)
    await state.update_data(ph_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('Physics',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'Physics'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з фізики було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'ph_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('Physics',))
        homework = cursor.fetchall()
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з фізики:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}', parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з фізики поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'en_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect("UsersData.sql")
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM members""")
        user_name = cursor.fetchall()
        conn.commit()
        conn.close()
        if call.from_user.username in str(user_name):
            await call.message.answer('Добре, запишемо домашнє завдання з англійської!\nНапиши сюди завдання')
            await state.set_state(Form.en_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.en_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    print(date)
    await state.update_data(en_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('English',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'English'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з англійської було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'en_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('English',))
        homework = cursor.fetchall()
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з англійської:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}',
                parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з англійської поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'uk_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect("UsersData.sql")
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM members""")
        user_name = cursor.fetchall()
        conn.commit()
        conn.close()
        if call.from_user.username in str(user_name):
            await call.message.answer('Добре, запишемо домашнє завдання з української мови!\nНапиши сюди завдання')
            await state.set_state(Form.uk_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.uk_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    print(date)
    await state.update_data(uk_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('Ukrainian',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'Ukrainian'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з української мови було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'uk_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('Ukrainian',))
        homework = cursor.fetchall()
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з української мови:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}',
                parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з української мвои поки що нема🥳🥳🥳!')


@dp.callback_query(lambda x: x.data == 'fr_add')
async def process_callback_button1(call: types.CallbackQuery, state: FSMContext):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect("UsersData.sql")
        cursor = conn.cursor()
        cursor.execute("""SELECT user_name FROM members""")
        user_name = cursor.fetchall()
        conn.commit()
        conn.close()
        if call.from_user.username in str(user_name):
            await call.message.answer('Добре, запишемо домашнє завдання з французької мови!\nНапиши сюди завдання')
            await state.set_state(Form.fr_homework)
        elif call.from_user.username not in user_name:
            await call.message.answer('Ви ще не зареєструвалися!\nНапиши <b><i>/reg</i></b> для того щоб '
                                      'зареєструватися', parse_mode='HTML')


@dp.message(Form.fr_homework)
async def set_homework(message: types.Message, state: FSMContext):
    d = str(datetime.date.today()).split('-')
    date = str(d[0] + '.' + d[1] + '.' + d[2])

    print(date)
    await state.update_data(fr_homework=message.text)

    if message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR IGNORE INTO dz (subject) VALUES (?)''',
                       ('French',))
        cursor.execute('''UPDATE OR IGNORE dz SET homework=?, today=? WHERE subject=?''',
                       (message.text, date, 'French'))
        conn.commit()
        conn.close()
        await message.answer('Домашку з французької мови було записано!')
        await state.clear()
    else:
        return


@dp.callback_query(lambda x: x.data == 'fr_show')
async def process_callback_button2(call: types.CallbackQuery):
    if call.message.chat.type == 'private':
        conn = sqlite3.connect('UsersData.sql')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM dz WHERE subject=?''', ('French',))
        homework = cursor.fetchall()
        conn.commit()
        conn.close()
        if homework:
            await call.message.answer(
                f'Ось домашнє завдання з французької мови:\n  <b>{homework[0][2]}</b>\nДата: {homework[0][3]}',
                parse_mode='HTML')
        else:
            await call.message.answer('Домашнього завдання з французької мвои поки що нема🥳🥳🥳!')


@dp.message(F.text)
async def ans(message: types.Message):
    if message.chat.type == 'private':
        a = random.randint(1, 3)
        if a == 1:
            await message.answer('ПОМОГИТЕ!!!!! СОЗДАТЕЛЬ МЕНЯ ТРАХАЕТ! СПАСИТЕЕЕЕЕЕ')
        elif a == 2:
            await message.answer('Я сигма Я сигма Я сигма Я сигма Я сигма Я сигма😎😎😚☺️😚☺️')
        else:
            await message.answer_sticker('CAACAgIAAxkBAAEEWkBmBYjbznDO6e3mdgGAJ61reFJqAgACGzoAAuzFYUtipdVq8-DmSzQE')
    else:
        return


# Show db data
def db():
    conn = sqlite3.connect('UsersData.sql')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM members""")
    billy = cursor.fetchall()
    conn.commit()
    print(billy)
    cursor.execute('SELECT * FROM dz')
    oleg = cursor.fetchall()
    conn.commit()
    print(oleg)
    conn.close()


db()


@dp.message()
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
