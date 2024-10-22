import json

# Открываем файл на чтение
with open('categories.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

# Проходимся по всем элементам списка
for category, subcategories in categories.items():
    print(f'Категория: {category}')
    print(f'subcategories: {subcategories}')
    for subcategory, features in subcategories.items():
        print(f'Подкатегория: {subcategory}')
        if features:
            for feature in features:
                print(f': {feature}')
        else:
            print('Подкатегория не имеет особенностей')
