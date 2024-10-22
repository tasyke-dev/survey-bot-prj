from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def inline_keyboard_category(name_form=None, name_category=None, categories=None):
    if name_form == 'start':
        key_num = ()
        form = InlineKeyboardMarkup(row_width=4)
        number = 0
        for category, subcategories  in categories.items():
            number += 1
            key_num += (InlineKeyboardButton(number, callback_data=category[:23]+'_category'),)
        form.add(*key_num)
        return form
    elif name_form == 'category':
        key_num = ()
        form = InlineKeyboardMarkup()
        number = 0
        for category, subcategories in categories.items():
            if name_category in category:
                if subcategories is not None:
                    for subcategory, features in subcategories.items():
                        number += 1
                        key_num += (InlineKeyboardButton(number, callback_data=subcategory[:20]+'_subcategory'),)          
                    form.add(*key_num)
                    form.add(InlineKeyboardButton('🔙Назад', callback_data='subcategory_back'))    
                else:
                    form.add(InlineKeyboardButton('Ок', callback_data='category_ok'))
                    form.add(InlineKeyboardButton('🔙Назад', callback_data='category_OkBack'))
        return form
    elif name_form == 'subcategory':
        key_num = ()
        form = InlineKeyboardMarkup()
        number = 0
        for category, subcategories in categories.items():
            for subcategory, features in subcategories.items():
                if name_category in subcategory:
                    if features is not None:
                            for item in features:
                                number += 1
                                key_num += (InlineKeyboardButton(number, callback_data=item[:17]+'_subsubcategory'),)
                            form.add(*key_num)
                            form.add(InlineKeyboardButton('🔙Назад', callback_data='subsubcategory_back'))
                    else:
                        form.add(InlineKeyboardButton('Ок', callback_data='subcategory_ok'))
                        form.add(InlineKeyboardButton('🔙Назад', callback_data='subcategory_OkBack'))          
        return form
    elif name_form == 'subsubcategory':
        key_num = ()
        form = InlineKeyboardMarkup()
        form.add(InlineKeyboardButton('Ок', callback_data='subsubcategory_ok'))          
        form.add(InlineKeyboardButton('🔙Назад', callback_data='subsubcategory_OkBack'))
        return form
    