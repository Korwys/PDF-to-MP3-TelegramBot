from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btn_ru = InlineKeyboardButton('Русский', callback_data='ru')
btn_en = InlineKeyboardButton('Английский', callback_data='en')
btn_es = InlineKeyboardButton('Испаский', callback_data='es')
btn_pt = InlineKeyboardButton('Португальский', callback_data='pt')
btn_cz = InlineKeyboardButton('Чешский', callback_data='cz')
btn_it = InlineKeyboardButton('Итальянский', callback_data='it')
btn_kz = InlineKeyboardButton('Казахский', callback_data='kz')
btn_pl = InlineKeyboardButton('Польский', callback_data='pl')
btn_ro = InlineKeyboardButton('Румынский', callback_data='ro')
btn_th = InlineKeyboardButton('Тайский', callback_data='th')
btn_ae = InlineKeyboardButton('Арабский', callback_data='ar')
btn_cn = InlineKeyboardButton('Китайский', callback_data='cn')

inline_kb = InlineKeyboardMarkup().row(btn_ru, btn_en, btn_es, btn_pt). \
    row(btn_kz, btn_pl, btn_ro, btn_th).row(btn_cz, btn_it, btn_ae, btn_cn)
