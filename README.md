# ymaps
---------
[![PyPI Version][pypi-image]][pypi-url]
![GitHub][license]

**`ymaps`** - это клиент для [API Яндекс Карт](https://yandex.ru/dev/maps/mapsapi/) (Неофициальный)

Синхронные и Асинхронные:

* Search, SearchAsync - [Поиск по организациям](https://yandex.ru/dev/maps/geosearch/?from=mapsapi)
* Geocoder, GeocodeAsync - [Геокодер](https://yandex.ru/dev/maps/geocoder/?from=mapsapi)
* Suggest, SuggestAsync - [Геосаджест](https://yandex.ru/dev/maps/geosuggest/)
* Static, StaticAsync - [Static API](https://yandex.ru/dev/maps/staticapi/?from=mapsapi)



---------

## Установка

```
pip install ymaps
```

Зависимости
* python 3.7+
* [httpx](https://pypi.org/project/httpx/)

---------
## Использование

> Геокоординаты задаются в порядке долгота и широта

> \* - обязательный аргумент

> Все необязяательные аргументы должны передаваться по имени


### Параметры клиентов

#### Аргументы:
 - api_key*, [получить ключ](https://developer.tech.yandex.ru/)
 - language, язык ответа, по умолчанию русский (ru_RU)
 - timeout, таймаут запроса, по умолчанию 1 секунда


#### Примеры:
```
# api_key = 'api_key', language = 'en_RU', timeout = 10
Search('api_key', 'en_RU', 10)

# api_key = 'api_key', language = 'ru_RU', timeout = 1
Geocode('api_key')

# api_key = 'api_key', language = 'tr_TR', timeout = 1
Suggest('api_key').suggest(text, lang='tr_TR')
```


### [Search](https://yandex.ru/dev/geosearch/doc/ru/request)

Поиска по организациям и географическим объектам (топонимы), [формат ответа](https://yandex.ru/dev/geosearch/doc/ru/response).

#### search()

Выполняет поиск по организациям или топонимам.

- __text*__- текст поискового запроса
- __lang__ - язык ответа, по умолчанию ru_RU
- __type__ - типы возвращаемых результатов. geo — топонимы, biz — организации, по умолчанию автоматическое определение типа по тексту запроса
- __ll__ - центр области поиска
- __spn__ - размеры области поиска
- __bbox__ - альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным. Границы области поиска задаются в виде географических координат левого нижнего и правого верхнего углов области.
- __rspn__ - признак «жесткого» ограничения области поиска, по умолчанию False (не ограничивать)
- __results__ - количество возвращаемых объектов, по умолчанию 10
- __skip__ - количество объектов в ответе (начиная с первого), которое необходимо пропустить, skip должно нацело делиться на results
- __uri__ - Дополнительная информация об объекте, значение параметра возвращается в ответе Геосаджеста.

#### Примеры:
```
client = Search('api_key')


# text
client.search('лебединое озеро')
client.search('55.750788,37.618534')
client.search('Санкт-Петербург, ул. Блохина, 15')
client.search('+7 495 739-70-70')
client.search('ООО Яндекс')

# lang
client.search('ООО Яндекс', lang='ru_RU')
client.search('Санкт-Петербург, ул. Блохина, 15', lang='be_BY')

# type
client.search('ООО Яндекс', lang='ru_RU', type='biz')
client.search('лебединое озеро', type='geo')

# ll, spn (используются совместно)
client.search('площадь Революции', ll=[37.618920, 55.756994], spn=[0.552069, 0.400552])

# bbox
client.search('Театр', bbox=[36.83, 55.67, 38.24, 55.91])

# rspn, не искать за пределами заданной области
client.search('Театр', rspn=True, bbox=[36.83, 55.67, 38.24, 55.91])

# results
client.search('Администрация', results=25)

# skip
client.search('Администрация', results=25, skip=25)


# asynchronous
client = SearchAsync('api_key')
await client.search('ООО Яндекс', lang='ru_RU')
```

### [Geocode](https://yandex.ru/dev/geocode/doc/ru/request)

Прямое и обратное геокодирование, [формат ответа](https://yandex.ru/dev/geocode/doc/ru/response).

#### geocode()

Преобразует адрес в координаты объекта.

- __geocode*__ - текст поискового запроса
- __ll__ - центр области поиска
- __spn__ - размеры области поиска
- __bbox__ - альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным. Границы области поиска задаются в виде географических координат левого нижнего и правого верхнего углов области.
- __format__ - формат ответа геокодера xml, json; json по умолчанию
- __rspn__ - признак «жесткого» ограничения области поиска, по умолчанию False (не ограничивать)
- __results__ - количество возвращаемых объектов, по умолчанию 10
- __skip__ - количество объектов в ответе (начиная с первого), которое необходимо пропустить, skip должно нацело делиться на results
- __lang__ - язык ответа, по умолчанию ru_RU
- __uri__ - Дополнительная информация об объекте, значение параметра возвращается в ответе Геосаджеста.

#### reverse()

Преобразует координаты в адрес объекта.  Принимает те же аргументы что и geocode(), а также:

* __geocode*__ - географические координаты объекта
* __sco__ - порядок записи координат, longlat — долгота, широта, latlong — широта, долгота, по умолчанию longlat
* __kind__ - вид необходимого топонима (house, street, metro, district, locality), по умолчанию подбирается автоматически

#### Примеры:
```
client = Geocode('api_key')

# geocode
client.geocode('Санкт-Петербург, ул. Блохина, 15')

#reverse
client.reverse([37.611347, 55.760241])

# format, kind
client.reverse([37.611347, 55.760241], format='xml', kind='street')

# sco
client.reverse([55.760241, 37.611347], sco='latlong')

# ll, spn (используются совместно)
client.geocode('Санкт-Петербург, ул. Блохина, 15', ll=[30.301324, 59.951921], spn=[0.552069, 0.400552])

# bbox
client.geocode('Санкт-Петербург, ул. Блохина, 15', bbox=[36.83, 55.67, 38.24, 55.91])


# asynchronous
client = GeocodeAsync('api_key')
await client.geocode('Санкт-Петербург, ул. Блохина, 15')
```


### [Suggest](https://yandex.ru/dev/geosuggest/doc/ru/request)

Позволяет получать предложения поисковой выдачи во время поиска географических объектов и/или организаций, [формат ответа](https://yandex.ru/dev/geosuggest/doc/ru/response).

#### suggest()

Выполняет поиск по организациям или топонимам.

- __text*__- текст поискового запроса
- __lang__ - язык ответа в формате [ISO 639-1](https://www.loc.gov/standards/iso639-2/php/code_list.php), по умолчанию ru
- __results__ - количество возвращаемых объектов, по умолчанию 10
- __highlight__ - По умолчанию сервис осуществляет подсветку совпадений в результатах и возвращает набор диапазонов индексов, которые можно выделить в интерфейсе. Значение highlight=0 отключает подсветку.
- __ll__ - центр области поиска
- __spn__ - размеры области поиска
- __bbox__ - альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным. Границы области поиска задаются в виде географических координат левого нижнего и правого верхнего углов области.
- __ull__ - координаты пользователя, используется при расчете расстояний. Если параметр не указан, по умолчанию для расчетов будет взят центр окна.
- __strict_bounds__ - используется в значении strict_bounds=1, чтобы строго ограничить выдачу и оставлять только объекты, которые попадают в окно.
- __types__ - тип объекта в ответе
- __print_address__ - возвращает покомпонентный адрес в ответе. Для этого укажите значение print_address=1
- __org_address_kind__ - возвращает список организаций только с адресом до номера дома
- __attrs__ - используется в значении attrs=uri. Возвращает в ответе параметр uri

#### Примеры:
```
client = Suggest('api_key')


# text
client.suggest('санкт')

# lang
client.suggest('санкт', lang='be')

# types  
client.suggest('санкт', types='province')

# ll, spn (используются совместно)
client.suggest('площадь Революции', ll=[37.618920, 55.756994], spn=[0.552069, 0.400552])

# bbox, ull
client.suggest('Театр', bbox=[36.83, 55.67, 38.24, 55.91], ull=[36.84, 55.69])


# asynchronous
client = SearchAsync('api_key')
await client.search('ООО Яндекс', lang='ru_RU')
```


### [Static](https://yandex.ru/dev/staticapi/doc/ru/request)

Формирует изображение схемы карты

#### get_image()

Формирует изображение схемы карты в соответствии со значениями параметров,
возвращает bytes. 

__*__ - __ll__ или __bbox__

- __ll__ - центр области поиска, долгота и широта центра карты в градусах
- __bbox__ - альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным. Границы области поиска задаются в виде географических координат левого нижнего и правого верхнего углов области.
- __spn__ - протяженность области показа карты по долготе и широте (в градусах)
- __z__ - уровень масштабирования карты (0-17), см
- __size__ - ширина и высота запрашиваемого изображения карты (в пикселах)
- __scale__ - коэффициент увеличения объектов на карте (от 1.0 до 4.0)
- __pt__ - содержит описание одной или нескольких меток, которые требуется отобразить на карте
- __pl__ - Содержит набор описаний геометрических фигур (ломаных и многоугольников), которые требуется отобразить на карте

#### Примеры:

```
client = Static()

# ll
client.getimage(ll=[37.620070, 55.753630])

# spn
client.getimage(ll=[37.620070, 55.753630], spn=[0.02, 0.02])

# bbox
client.getimage(bbox=[30.03, 59.85, 30.49, 60.10])

# z scale
client.getimage(ll=[37.620070, 55.753630], z=12, scale=2.5)

# size 
client.getimage(ll=[37.620070, 55.753630], size=[450, 450])

# pt
client.getimage(ll=[37.620070, 55.753630], pt=[
	'37.620070,55.753630,pmwtm1', 
	'37.62006,55.753632,pmwtm2'
])

# pl
client.getimage(ll=[37.620070, 55.753630], pl=[
	'c:ec473fFF,f:00FF00A0,w:5,37.51,55.83', 
	'c:ec473fFF,f:00FF00A0,w:5,37.49,55.70,37.51,55.83'
])


# asynchronous
client = StaticAsync()
await client.getimage(ll=[37.620070, 55.753630])
```

Сохраните изображение:
```sh
response = Static('api_key').get_image(...)

with open('file.png', "wb") as f:
	f.write(response)
```

## Development setup

```sh
$ python3 -m venv venv
$ . venv/bin/activate
$ make deps
$ tox
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

<!-- Badges -->
[pypi-image]: https://img.shields.io/pypi/v/ymaps?color=blue
[pypi-url]: https://pypi.org/project/ymaps/

[license]: https://img.shields.io/github/license/sfkan6/ymaps