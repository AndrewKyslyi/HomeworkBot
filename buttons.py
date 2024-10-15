from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

algebra_btn = InlineKeyboardButton(text='Алгебра🔢', callback_data='algebra')
algebra_add = InlineKeyboardButton(text='Записати✒️', callback_data='al_add')
algebra_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='al_show')

geometry_btn = InlineKeyboardButton(text='Геометрія📐', callback_data='geometry')
geometry_add = InlineKeyboardButton(text='Записати✒️', callback_data='gm_add')
geometry_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='gm_show')

chemistry_btn = InlineKeyboardButton(text='Хімія🧪', callback_data='chemistry')
chemistry_add = InlineKeyboardButton(text='Записати✒️', callback_data='ch_add')
chemistry_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='ch_show')

physics_btn = InlineKeyboardButton(text='Фізика🔭', callback_data='physics')
physics_add = InlineKeyboardButton(text='Записати✒️', callback_data='ph_add')
physics_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='ph_show')

english_btn = InlineKeyboardButton(text='Английська мова💷', callback_data='english')
english_add = InlineKeyboardButton(text='Записати✒️', callback_data='en_add')
english_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='en_show')

ukrainian_btn = InlineKeyboardButton(text='Українська мова🩵💛', callback_data='ukrainian')
ukrainian_add = InlineKeyboardButton(text='Записати✒️', callback_data='uk_add')
ukrainian_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='uk_show')

french_btn = InlineKeyboardButton(text='Французька мова🥐', callback_data='french')
french_add = InlineKeyboardButton(text='Записати✒️', callback_data='fr_add')
french_show = InlineKeyboardButton(text='Дізнатися🤔⁉️', callback_data='fr_show')

subjects = InlineKeyboardMarkup(inline_keyboard=[[algebra_btn], [algebra_add, algebra_show],
                                                 [geometry_btn], [geometry_add, geometry_show],
                                                 [chemistry_btn], [chemistry_add, chemistry_show],
                                                 [physics_btn], [physics_add, physics_show],
                                                 [english_btn], [english_add, english_show],
                                                 [ukrainian_btn], [ukrainian_add, ukrainian_show],
                                                 [french_btn], [french_add, french_show]])
