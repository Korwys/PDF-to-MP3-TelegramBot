import urllib

from aiogram.dispatcher import FSMContext
from aiogram import types, executor
from aiogram.types import ContentType

from config.bot import dp, token, bot, LangState
from config import keybords as kb
from services.gtts import make_convert


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message) -> None:
    """По команде /start отправляет пользователю приветственное сообщение"""
    await message.reply(f"Привет, {message.chat.first_name}. Для начала работы с файлом наберите /new.")


@dp.message_handler(commands=['new'])
async def start_message(message: types.Message) -> None:
    """По команде /new просит пользователя выбрать язык текста из документа"""
    await bot.send_message(message.chat.id, 'Для начала выбери язык текста в твоем документе.',
                           reply_markup=kb.inline_kb)


@dp.callback_query_handler(lambda c: c.data)
async def process_callbacks(callback_query: types.CallbackQuery, state: FSMContext):
    """Функция срабатывает при выборе языка. Сохраняет выбранный язык в state 'lang'  и запрашивает файл и пользователя"""
    code = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await LangState.lang.set()
    await state.update_data(lang=code)
    await bot.send_message(callback_query.from_user.id, 'Супер. Теперь скидывай файл с текстом')
    await state.reset_state(with_data=False)


@dp.message_handler(content_types=['document'])
async def make_audio_from_pdf(message: types.Message, state: FSMContext) -> None:
    """Функция срабатывает при отправке пользователем файла боту. Получает state 'lang' выбранный пользователем ранее,
    созраняет файл, конвертирует из текста в аудио и отправляет пользователю готовый аудио файл"""
    data = await state.get_data()
    document_id = message.document.file_id
    await message.reply(f'Спасибо {message.chat.first_name}!')
    file_info = await bot.get_file(document_id)
    path_f = f'./media/{message.document.file_name}'
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{token}/{file_info.file_path}',
                               f'./media/{message.document.file_name}')
    await bot.send_message(message.from_user.id, 'Файл успешно сохранён. Начинаю готовить звуковую дорожку... ')
    audio_file_path = await make_convert(file_path=path_f, lang=data['lang'])
    audio_file = open(audio_file_path, 'rb')
    await bot.send_audio(chat_id=message.chat.id, audio=audio_file)
    await bot.send_message(message.chat.id, 'Файл готов. Если нужно обработать еще один файл напиши - /new')


@dp.message_handler(content_types=ContentType.PHOTO or ContentType.AUDIO or ContentType.VOICE or ContentType.UNKNOWN)
async def wrong_format(message: types.Message):
    """Если пользователь отправил не DOCUMENT, то его сообщение будет удалено и бот отправит сообщение
    с поддердиваемыми форматами файлов"""
    await bot.send_message(message.from_user.id,
                           'Неверный формат файла. Файл удален. Поддерживаемые форматы: PDF,DOC,DOCX')
    await bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
