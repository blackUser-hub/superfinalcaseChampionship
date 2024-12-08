import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

# Ваш токен бота
API_TOKEN = "7455607693:AAFId00IZ3pZqHrD1dhD3cbf2ie7ECaw2s4"

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Где мы")],
        [KeyboardButton(text="Кто мы")],
        [KeyboardButton(text="Наши соц сети")],
        [KeyboardButton(text="Видео представление")],
    ],
    resize_keyboard=True,
)

# Проверка существования файла и его размера
def check_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    file_size = os.path.getsize(file_path)
    return file_size

# Хэндлер для команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Добро пожаловать в GN Studio! Выберите интересующую вас информацию:",
        reply_markup=keyboard,
    )

# Хэндлер для кнопки "Где мы"
@router.message(lambda msg: msg.text == "Где мы")
async def location_handler(message: types.Message):
    await message.answer("Мы находимся здесь: https://yandex.ru/maps/-/CHAd7VOC")

# Хэндлер для кнопки "Кто мы"
@router.message(lambda msg: msg.text == "Кто мы")
async def about_handler(message: types.Message):
    photo_path = "gnstudio_image.jpg"  # Укажите правильный путь к изображению
    try:
        photo = FSInputFile(photo_path)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption="Привет, дорогой друг! 🌟\n\nХотим радостью поделиться нашей студией-музеем искусственного интеллекта в Москве! Это не просто музей — это целый мир, где искусство и технологии переплетаются, создавая удивительные эмоции и новые идеи!"
        )
    except FileNotFoundError:
        await message.answer("Файл изображения не найден. Проверьте путь.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

# Хэндлер для кнопки "Наши соц сети"
@router.message(lambda msg: msg.text == "Наши соц сети")
async def social_links_handler(message: types.Message):
    await message.answer(
        "Наши соц сети:\n"
        "Telegram: https://t.me/gnstudio_museum\n"
        "Сайт: https://beivbrwbvow.my.canva.site/gn-studio"
    )

# Хэндлер для кнопки "Видео представление"
@router.message(lambda msg: msg.text == "Видео представление")
async def video_handler(message: types.Message):
    try:
        await bot.send_message(chat_id=message.chat.id, text="Подождите пару секунд...")
        # Путь к файлу видео
        video_path = "rrr.mp4"
        video_size = check_file(video_path)

        # Отправка видео
        video = FSInputFile(video_path)
        await bot.send_video(
            chat_id=message.chat.id,
            video=video,
            caption="Добро пожаловать в мир искусственного интеллекта! 🌟\nЭто видео — ваш первый шаг в захватывающее путешествие по нашей студии-музею"
        )
        await bot.send_message(chat_id=message.chat.id, text="Более подробно узнать о нас можно по ссылке:  https://t.me/GNSExcurs/2")
    except FileNotFoundError as e:
        await message.answer(str(e))
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

# Регистрация маршрутов
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
