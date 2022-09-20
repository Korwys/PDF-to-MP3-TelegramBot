import urllib
from pathlib import Path

from gtts import gTTS
import pdfplumber
from aiogram import types, executor

from config.bot import dp, token, bot


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
    await message.reply('Скиньте pdf файл')


@dp.message_handler(content_types=['document'])
async def make_audio_from_pdf(message: types.Message):
    document_id = message.document.file_id
    await message.reply(f'Спасибо {message.chat.first_name}!')
    file_info = await bot.get_file(document_id)
    path_f = f'./media/{message.document.file_name}'
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{token}/{file_info.file_path}',
                               f'./media/{message.document.file_name}')
    await bot.send_message(message.from_user.id, 'Файл успешно сохранён. Начинаю готовить звуковую дорожку... ')
    audio_file_path = await make_convert(file_path=path_f, lang='en')
    audio_file = open(audio_file_path, 'rb')
    await bot.send_audio(chat_id=message.chat.id, audio=audio_file)


async def make_convert(file_path='test.pdf', lang='en') -> str:
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            text = ''.join(pages)
            text = text.replace('\n', '')

        audio = gTTS(text=text, lang=lang, slow=False)
        file_name = Path(file_path).stem
        audio.save(f'./mp3/{file_name}.mp3')
        audio_file = f'./mp3/{file_name}.mp3'
        return audio_file



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
