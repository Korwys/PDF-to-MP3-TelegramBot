from pathlib import Path

import pdfplumber
from gtts import gTTS
from docx import Document


async def make_convert(file_path='test.pdf', lang='en') -> str:
    """ Опеределяет формат документа, распаршивает его и передает функции conver_text_speech"""
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            pdf_text = ''.join(pages)
            pdf_text = pdf_text.replace('\n', '')

        return convert_text_to_speech(text=pdf_text, lang=lang, file_path=file_path)
    elif Path(file_path).is_file() and Path(file_path).suffix == '.doc' or 'docx':
        doc = Document(file_path)
        docx_text = [paragraph.text for paragraph in doc.paragraphs]
        docx_text = ''.join(docx_text).replace('\n', '')

        return convert_text_to_speech(text=docx_text, lang=lang, file_path=file_path)


def convert_text_to_speech(text: str, lang: str, file_path: str) -> str:
    """Конвертирует текстовый файл в аудио файл и сохраняет его"""
    audio = gTTS(text=text, lang=lang, slow=False)
    file_name = Path(file_path).stem
    audio.save(f'./mp3/{file_name}.mp3')
    audio_file = f'./mp3/{file_name}.mp3'
    return audio_file
