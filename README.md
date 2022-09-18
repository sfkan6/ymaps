# ymaps
---------
[![PyPI Version][pypi-image]][pypi-url]
![GitHub][license]

**`ymaps`** - это клиент для [API Яндекс Карт](https://yandex.ru/dev/maps/mapsapi/) (Неофициальный)

Синхронные и Асинхронные:

* SearchClient, SearchAsync - [Поиск по организациям](https://yandex.ru/dev/maps/geosearch/?from=mapsapi)
* GeocoderClient, GeocodeAsync - [Геокодер](https://yandex.ru/dev/maps/geocoder/?from=mapsapi)
* StaticClient, StaticAsync - [Static API](https://yandex.ru/dev/maps/staticapi/?from=mapsapi)



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


### Клиенты
#### Аргументы:
 - api_key*, [получить ключ](https://developer.tech.yandex.ru/).
 - timeout, таймаут запроса, по умолчанию 1 секунда.
 - lang, язык ответа, по умолчанию русский (ru_RU), если в методе передан 'tr_TR', то будет использован 'tr_TR', но только для этого запроса.


> api_key в StaticClient необязателен, указывайте только если используете коммерческую версию.


#### Примеры:
```
# api_key = 'key', timeout = 10, lang = 'en_RU'
SearchClient('key', 10, 'en_RU')

# api_key = 'key', timeout = 1, lang = 'ru_RU'
GeocoderClient('key')

# api_key = None, timeout = 1, lang = 'ru_RU'
StaticClient() # api_key=None, timeout=1, lang='ru_RU'
```

### [SearchClient](https://yandex.ru/dev/maps/geosearch/doc/concepts/request.html)
Поиска по организациям и географическим объектам (топонимы), 
[формат ответа](https://yandex.ru/dev/maps/geosearch/doc/concepts/response_structure_toponyms.html).
#### search()

Выполняет поиск по организациям или топонимам.

- __query*__, текст поискового запроса
- __lang__, язык ответа, по умолчанию ru_RU
- __type__, типы возвращаемых результатов. geo — топонимы, biz — организации, по умолчанию автоматическое определение типа по тексту запроса
- __ll__, центр области поиска
- __spn__, размеры области поиска
- __bbox__, альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным
- __rspn__, признак «жесткого» ограничения области поиска, по умолчанию False (не ограничивать)
- __results__, количество возвращаемых объектов, по умолчанию 10
- __skip__, количество объектов в ответе (начиная с первого), которое необходимо пропустить, skip должно нацело делиться на results

#### Примеры:
```
client = SearchClient('api_key')


# query
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

### [GeocoderClient](https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/input_params.html)

Прямое и обратное геокодирование, [формат ответа](https://yandex.ru/dev/maps/geocoder/doc/desc/reference/response_structure.html).
#### geocode()

Преобразует адрес в координаты объекта.

- __geocode*__, текст поискового запроса
- __rspn__, признак «жесткого» ограничения области поиска, по умолчанию False (не ограничивать)
- __ll__, центр области поиска
- __spn__, размеры области поиска
- __bbox__, альтернативный способ задания области поиска, при одновременном задании bbox и ll+spn параметр bbox является более приоритетным
- __format__, формат ответа геокодера xml, json; json по умолчанию 
- __results__, количество возвращаемых объектов, по умолчанию 10
- __skip__, количество объектов в ответе (начиная с первого), которое необходимо пропустить, skip должно нацело делиться на results
- __lang__, язык ответа, по умолчанию ru_RU

#### reverse()

Преобразует координаты в адрес объекта.  Принимает те же аргументы что и geocode() и еще:

* __geocode*__, географические координаты объекта
* __sco__, порядок записи координат, longlat — долгота, широта, latlong — широта, долгота, по умолчанию longlat
* __kind__, вид необходимого топонима (house, street, metro, district, locality)

#### Примеры:
```
client = GeocoderClient('api_key')

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

### [StaticClient](https://yandex.ru/dev/maps/staticapi/doc/1.x/dg/concepts/input_params.html)

Формирует изображение карты в соответствии со значениями параметров,
возвращает bytes.

#### getimage()

- __ll*__, центр области поиска, долгота и широта центра карты в градусах
- __l*__, перечень слоев, определяющих тип карты: map (схема), sat (спутник), sat,skl (гибрид), trf (Слой пробок)
- __spn__, протяженность области показа карты по долготе и широте (в градусах)
- __z__, уровень масштабирования карты (0-17), см
- __size__, ширина и высота запрашиваемого изображения карты (в пикселах)
- __scale__, коэффициент увеличения объектов на карте (от 1.0 до 4.0)
- __pt__, содержит описание одной или нескольких меток, которые требуется отобразить на карте
- __pl__, Содержит набор описаний геометрических фигур (ломаных и многоугольников), которые требуется отобразить на карте
- __lang__, язык ответа, по умолчанию ru_RU

#### Примеры:

```
client = StaticClient()

# l
client.getimage([37.620070, 55.753630], l=['sat', 'skl'])

# spn
client.getimage([37.620070, 55.753630], l=['sat', 'trf'], spn=[0.02, 0.02])

# z scale
client.getimage([37.620070, 55.753630], z=12, scale=2.5)

# size 
client.getimage([37.620070, 55.753630], size=[450, 450])

# pt
client.getimage([37.620070, 55.753630], pt=['37.620070,55.753630,pmwtm1', '37.62006,55.753632,pmwtm2'])

# pl
client.getimage([37.620070, 55.753630], pl=['c:ec473fFF,f:00FF00A0,w:5,37.51,55.83', 'c:ec473fFF,f:00FF00A0,w:5,37.49,55.70,37.51,55.83'])


# asynchronous
client = StaticAsync()
await client.getimage([37.620070, 55.753630], l=['sat', 'skl'])
```

Сохраните изображение:
```sh
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