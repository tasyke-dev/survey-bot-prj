import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import MediaGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from categoryHandler import *
from smileHandler import *

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)


API_TOKEN = ''

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

with open('categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

# Определение состояний для машины состояний
class Form(StatesGroup):
    location = State() # Местоположение на геолокации
    category = State() # Выбор категории
    comment = State() # Комментарий
    media = State() # Фото или видео
    ratingSmile = State() # Оценка смайликом
    hashtag = State() # ХешТег

# Обработка команды /start
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Создать')).add(KeyboardButton('Информация'))
    await bot.send_message(chat_id= message.from_user.id, text='Здравствуй .👋 \n...', reply_markup=keyboard)

#Выход из состояний
@dp.message_handler(state="*", commands='🔙Отмена')
@dp.message_handler(Text(equals='🔙Отмена', ignore_case = True), state="*")
async def cancel_handler(message: types.Message, state):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer('Возможно вы ввели неправильную команду.')
        return
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Создать')).add(KeyboardButton('Информация'))
    await bot.send_message(message.from_user.id, 'Отменено', reply_markup=keyboard)
    await state.finish()

@dp.message_handler(commands='Информация')
async def cmd_start(message: types.Message):
    await message.answer('Мб впихнуть инфу по использыванию бота и сайт')

#Создать напоминание
@dp.message_handler(text='Создать')
async def cancel_handler(message: types.Message, state):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('🔙Отмена'))
    # Запуск машины состояний с начальным состоянием
    await Form.location.set()
    await bot.send_message(message.from_user.id, 'Привет! Где ты сейчас находишься? (Отправь геолокацию)', reply_markup=keyboard)

# Обработка геолокации
@dp.message_handler(content_types=['any'], state=Form.location)
async def process_wrong_location(message: types.Message, state: FSMContext):
    if message.content_type != 'location':
        await message.reply("Пожалуйста, отправьте геолокацию")
        return
    # Сохранение местоположения в состоянии
    async with state.proxy() as data:
        data['location'] = message.location
    # Создание инлайн клавиатуры для выбора категорий
    ansMsg = 'Выберите категорию:\n\n'
    if categories:
        number = 0
        for category, subcategories  in categories.items():
                ansMsg += str(number + 1) + '. ' + category + '\n'
                number += 1
        ansMsg += '\n'
        ansMsg += 'Нажмите на номер нужной категории:👇'
        form = inline_keyboard_category('start', ' ', categories)
        await bot.send_message(message.from_user.id, ansMsg, reply_markup=form)
    # Переход к следующему состоянию
    await Form.next()

# Обработка категории
@dp.callback_query_handler(state=Form.category)
async def process_category(call: types.CallbackQuery, state: FSMContext):
    if call.data.split('_')[1] == 'category':
        # Сохранение категории в состоянии
        async with state.proxy() as data:
            data['category'] = call.data.split('_')[0]
            number = 0
            ansMsg = 'Выберите категорию:\n\n'
            for category, subcategories in categories.items():
                if call.data.split('_')[0] in category:
                    if subcategories is not None:
                        for subcategory, features in subcategories.items():
                            ansMsg += str(number + 1) + '. ' + subcategory + '\n'
                            number += 1
                        ansMsg += '\n'
                        ansMsg += 'Нажмите на номер нужной категории:👇'
                    else:
                        ansMsg = f'Вы выбрали категорию {category}.\nНажмите "Ок" чтобы продолжить.'
            await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
            inlkb = inline_keyboard_category('category', call.data.split('_')[0], categories)
            #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
            await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
    elif call.data.split('_')[1] == 'subcategory':
        # Сохранение категории в состоянии
        async with state.proxy() as data:
            data['subcategory'] = call.data.split('_')[0]
            number = 0
            ansMsg = 'Выберите категорию:\n\n'
            for category, subcategories in categories.items():
                if data['category'] in category:
                    for subcategory, features in subcategories.items():
                        if call.data.split('_')[0] in subcategory:
                            if features is not None:
                                for item in features:
                                    ansMsg += str(number + 1) + '. ' + item + '\n'
                                    number += 1
                                ansMsg += '\n'
                                ansMsg += 'Нажмите на номер нужной категории:👇'
                            else:
                                ansMsg = f'Вы выбрали категорию {subcategory}.\nНажмите "Ок" чтобы продолжить.'
            await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
            inlkb = inline_keyboard_category('subcategory', call.data.split('_')[0], categories)
            #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
            await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
    elif call.data.split('_')[1] == 'subsubcategory':
        # Сохранение категории в состоянии
        async with state.proxy() as data:
            data['subsubcategory'] = call.data.split('_')[0]
            for category, subcategories in categories.items():
                if data['category'] in category:
                    for subcategory, features in subcategories.items():
                        if data['subcategory'] in subcategory:
                                for item in features:
                                    if call.data.split('_')[0] in item:
                                        ansMsg = f'Вы выбрали категорию {item}.\nНажмите "Ок" чтобы продолжить.'
            await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
            inlkb = inline_keyboard_category('subsubcategory', call.data.split('_')[0], categories)
            #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
            await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
    elif call.data.split('_')[1] == 'back':
        if call.data.split('_')[0] == 'subcategory':
            async with state.proxy() as data:
                number = 0
                ansMsg = 'Выберите категорию:\n\n'
                for category, subcategories in categories.items():
                    ansMsg += str(number + 1) + '. ' + category + '\n'
                    number += 1
                ansMsg += '\n'
                ansMsg += 'Нажмите на номер нужной категории:👇'
                await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
                inlkb = inline_keyboard_category('start', ' ', categories)
                await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
        elif call.data.split('_')[0] == 'subsubcategory':
            async with state.proxy() as data:
                number = 0
                ansMsg = 'Выберите категорию:\n\n'
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        for subcategory, features in subcategories.items():
                            ansMsg += str(number + 1) + '. ' + subcategory + '\n'
                            number += 1
                ansMsg += '\n'
                ansMsg += 'Нажмите на номер нужной категории:👇'
                await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
                inlkb = inline_keyboard_category('category', data['category'], categories)
                await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
    elif call.data.split('_')[1] == 'OkBack':
        if call.data.split('_')[0] == 'category':
            async with state.proxy() as data:
                number = 0
                ansMsg = 'Выберите категорию:\n\n'
                for category, subcategories in categories.items():
                    ansMsg += str(number + 1) + '. ' + category + '\n'
                    number += 1
                ansMsg += 'Нажмите на номер нужной категории:👇'
                await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
                inlkb = inline_keyboard_category('start', ' ', categories)
                #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
                await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
        elif call.data.split('_')[0] == 'subcategory':
            async with state.proxy() as data:
                number = 0
                ansMsg = 'Выберите категорию:\n\n'
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        for subcategory, features in subcategories.items():
                            ansMsg += str(number + 1) + '. ' + subcategory + '\n'
                            number += 1
                        ansMsg += 'Нажмите на номер нужной категории:👇'
                await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
                inlkb = inline_keyboard_category('category', data['category'], categories)
                #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
                await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb) 
        elif call.data.split('_')[0] == 'subsubcategory':
            async with state.proxy() as data:
                number = 0
                ansMsg = 'Выберите категорию:\n\n'
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        for subcategory, features in subcategories.items():
                            if data['subcategory'] in subcategory:
                                if features is not None:
                                    for item in features:
                                        ansMsg += str(number + 1) + '. ' + item + '\n'
                                        number += 1
                                    ansMsg += '\n'
                                    ansMsg += 'Нажмите на номер нужной категории:👇'
                await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
                inlkb = inline_keyboard_category('subcategory', data['subcategory'], categories)
                #Изменение клавиатуры. Id пользователя, Id сообщения, новая форма
                await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=inlkb)
    elif call.data.split('_')[1] == 'ok':
        async with state.proxy() as data:
            if call.data.split('_')[0] == 'category':
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        data['category_output'] = category
            elif call.data.split('_')[0] == 'subcategory':
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        for subcategory, features in subcategories.items():
                            if data['subcategory'] in subcategory:
                                data['category_output'] = subcategory
            else:
                for category, subcategories in categories.items():
                    if data['category'] in category:
                        for subcategory, features in subcategories.items():
                            if data['subcategory'] in subcategory:
                                for item in features:
                                    if data['subsubcategory'] in item:
                                        data['category_output'] = item
            # data['media'] = list() 
            # data['media_group'] = None
            # data['state'] = False
            # Переход к следующему состоянию
            ansMsg = "Отправьте комментарий"
            await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
            await Form.next()       

# Обработка комментария
@dp.message_handler(state=Form.comment)
async def process_comment(message: types.Message, state: FSMContext):
    # Сохранение комментария в состоянии
    async with state.proxy() as data:
        data['comment'] = message.text
        # Получение всех данных из состояния
        # location = data['location']
        # category = data['category_output']
        # media = data['media']
        # comment = data['comment']
        data['media'] = list() 
        data['media_group'] = None
        data['state'] = False
        # Переход к следующему состоянию
        ansMsg = "Отправьте фото (от 1 до 10 штук) либо видео (до 10 секунд) и нажмите кнопку Готово"
        keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Готово')).add(KeyboardButton('🔙Отмена'))
        await bot.send_message(chat_id= message.from_user.id, text=ansMsg, reply_markup=keyboard)
        await Form.next()
    # Отправка сообщения с данными
    # await bot.send_message(chat_id=message.chat.id, text=f"Местоположение: {location}\nКатегория: {category}\nКомментарий: {comment}")
    # Отправка медиафайлов
    # for file in media:
    #     await bot.send_media_group(chat_id=message.chat.id, media=[file])
    # Завершение работы машины состояний
    # await state.finish()
    # keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Создать')).add(KeyboardButton('Информация'))
    # await bot.send_message(chat_id= message.from_user.id, text='Спасибо за информацию!', reply_markup=keyboard)

# Обработка медиа
@dp.message_handler(content_types=['photo', 'video', 'text'], state=Form.media)
async def process_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Проверка типа медиафайла
        if data['state']:
            data['media'] = list()
        if message.media_group_id:  
            if message.photo:
                if data['media'] == []:
                    if data['media_group'] != message.media_group_id:
                        data['state'] = False
                    file_info = message.photo.pop()   
                    data['media'].append(file_info['file_id'])
                    data['media_group'] = message.media_group_id          
                elif data['media_group'] != message.media_group_id:
                    data['media'] = list()
                    data['media_group'] = None
                    await message.reply("Ошибка: в одном сообщении можно отправить от 1 до 10 фотографий либо 1 видео до 10 секунд.")
                    return
                else:
                    file_info = message.photo.pop() 
                    data['media'].append(file_info['file_id']) 
            else:
                data['state'] = True
                await message.reply("⚠️В одном сообщении можно отправить от 1 до 10 фотографий либо 1 видео до 10 секунд.")
                return 
        elif message.text == 'Готово':
            if data['media'] != list(): 
                data['media_type'] = 'photo'
                form = inline_keyboard_smile()
                await bot.send_message(message.from_user.id, "Оцените от 1 до 5", reply_markup=form)
                await Form.next()
            else:
                await message.reply("Ошибка: сначала отправте от 1 до 10 фотографий либо 1 видео до 10 секунд.")        
        elif message.photo:
            if type(message.photo) != types.PhotoSize:
                await message.reply("Ошибка: можно отправлять только фото")
                return
            data['media_type'] = 'photo'
            data['media'] = message.photo.pop()['file_id'] 
            form = inline_keyboard_smile()
            await bot.send_message(message.from_user.id, "Оцените от 1 до 5", reply_markup=form)
            await Form.next()
        elif message.video:
            if message.video.duration > 10:
                await message.reply("Ошибка: видео должно быть не длиннее 10 секунд")
                return
            data['media_type'] = 'video'
            data['media'] = message.video['file_id']
            form = inline_keyboard_smile()
            await bot.send_message(message.from_user.id, "Оцените от 1 до 5", reply_markup=form)
            await Form.next()
        else:
            await message.reply("Ошибка: можно отправлять только фото или видео")
            return

# Обработка смайл рейтинга
@dp.callback_query_handler(state=Form.ratingSmile)
async def process_category(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if call.data.split('_')[0] == 1:
            data['ratingSmile'] = '😡'
        elif call.data.split('_')[0] == 2:
            data['ratingSmile'] = '🙁'
        elif call.data.split('_')[0] == 3:
            data['ratingSmile'] = '😐'
        elif call.data.split('_')[0] == 4:
            data['ratingSmile'] = '😏'
        else:
            data['ratingSmile'] = '😄'
        ansMsg = "Напишите ХешТеги которые могут быть привязаны к вашей записи."
        await bot.edit_message_text(ansMsg, call.from_user.id, call.message.message_id)
        await Form.next()

# Обработка ХешТега
@dp.message_handler(content_types=['any'], state=Form.hashtag)
async def process_comment(message: types.Message, state: FSMContext):
    if message.content_type != 'text':
        await message.reply("Пожалуйста, отправьте текст ХешТега.")
        return
    async with state.proxy() as data:
        # Получение всех данных из состояния
        location = data['location']
        category = data['category_output']
        media = data['media']
        comment = data['comment']
        raitingSmile = data['ratingSmile']
    await state.finish()
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True).add(KeyboardButton('Создать')).add(KeyboardButton('Информация'))
    await bot.send_message(chat_id= message.from_user.id, text='Спасибо за информацию!', reply_markup=keyboard)


#Вывод несуществующих команд
@dp.message_handler()
async def cancel_handler(message: types.Message, state):
    await message.answer('Возможно вы ввели неправильную команду.')

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)