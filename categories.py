import json


categories = {
    'Здание/дом/сооружение': {
        'Снаружи': {
            'Вход/дверь': None,
            'Крыша/сосульки': None,
            'Стены': None,
            'Лестница': None,
            'Окна': None,
            'Кондиционеры/тарелки/антенны': None,
            'Балкон': None,
            'Водосток': None,
        },
        'Внутри': {
            'Подъезд/холл/площадка': None,
            'Лифт': None,
            'Стены/потолок': None,
            'Пол/лестница': None,
            'Дверь/окно': None,
            'Мебель/почтовые ящики': None,
        },
    },
    'Улица': {
        'Транспортное средство': {
            'Автобус/общественный транспорт': None,
            'Легковой автомобиль': None,
            'Самокат': None,
            'Велосипед': None,
            'Мотоцикл': None,
            'Грузовая/строительная/спецтехника': None,
        },
        'Проезжая часть': {
            'Автодорога': None,
            'Парковка': None,
            'Рельсы': None,
            'Велодорожка': None,
            'Люк/ливневый сток': None,
            'Знак': None,
            'Светофор': None,
            'Столб/фонарь': None,
        },
        'Тротуар': {
            'Покрытие': None,
            'Люк': None,
            'Ступеньки/лестницы': None,
            'Столб/фонарь': None,
            'Пандус': None,
            'Тумбы/кашпо/столбики': None,
        },
        'Пешеходный переход': {
            'Надземный': None,
            'Подземный': None,
            'Зебра': None,
            'Светофор': None,
        },
        'Забор': None,
        'Рекламная конструкция': None,
    },
    'Двор/площадь/парк/общественное пространство': {
        'Фонтан': None,
        'Уличная мебель': None,
        'Детская площадка': None,
        'Спортивная площадка': None,
        'Мусорный бак': None,
        'Памятник/МАФ': None,
        'Столб/фонарь': None,
        'Техническое сооружение': None,
    },
    "Коммуникации": {
        "Вода": None,
        "Электричество": None,
        "Свет": None,
        "Газ": None,
        "Связь": None,
        "Трубы в целом": None,
        "Провода в целом": None,
        "Столб": None
    },
    "Животные": {
        "Собака": None,
        "Кошка": None,
        "Птица": None,
        "Дикий зверь": None,
        "Крысы/змеи": None,
        "Насекомые": None
    },
    "Растения/природа": {
        "Дерево": None,
        "Куст": None,
        "Трава/поле/пространство": None,
        "Цветы/клумба": None,
        "Водоем": None,
        "Овраг/рельеф": None,
        "Воздух": None,
        "Пляж": None
    },
    "Заведения/учреждения": {
        "Магазин/рынок/лавка/киоск": None,
        "Бар/клуб": None,
        "Кафе/столовая/общепит": None,
        "МФЦ/администрация": None,
        "Музей/театр/библиотека": None,
        "АЗС/шиномонтаж/автоуслуги": None,
        "Бытовые услуги": None,
        "ТЦ/ТРЦ/ТРК": None
    },
    "Непорядок": {
        "Куча мусора/снега/хлама/стройматериала": None,
        "Снег/лед": None,
        "Складированные стройматериалы": None,
        "Сосульки": None,
        "Граффити": None,
        "Лужа/непролазная грязь": None,
        "Стройплощадка": None,
        "Яма/котлован": None
    }
}


with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False)