Telegram бот для конвертации PDF и DOC текстовых файлов в mp3. 
Для преобразования текста из файла в аудио используется библитека gTTS (Google Text-to-Speech).

В переменных окружения надо проставить ваш API токен бота.

TOKEN = API токен бота

Запуск бота при помощи Docker:
 - Указать API TOKEN боты в переменной окружения
 - docker build -t pdfbot ./
 - docker run -d --restart allways pdfbot