Использован подход, описанный в статье 
"Training Deep AutoEncoders for Collaborative Filtering"(https://arxiv.org/abs/1708.01715)

## 1. Терминология

##### 1.1 Модель Адео
  Обученный алгоритм, делающий прогнозы и рекомендации, в сфере машинного обучения, принято называть Моделью.
  Однако, в компании LeroyMerlin Моделью принято называть Четко регламентированную категорию товаров, утвержденную ADEO. 
В связи с тем, что алгоритм опирается на активное использование Моделей Адео, данное слово Модель будет использоваться только в значении Товарной категории Адео.
  
##### 1.2 Автоэнкодер

Обученный алгоритм, который в сфере машинного обучения называется моделью.
Ввиду того, что мы используем Автоэнкодер для создания модели,
и чтобы не путаться с моделью Адео, будем использовать слово Автоэнкодер
Мы обучаем Автоэнкодер, и Автоэнкодер делает прогнозы.
  
##### 1.3 Проект клиента
  
То, что сейчас делает клиент. 
Ремонт дома, строительство сарая, установка окна, ремонт протекающего бачка унитаза, это все проект.
Покупка рамки для картины - проект Украшение стены.
Покупка монтажной пены каждый месяц - возможно, проект Установки окон для клиентов (например, у бригад)
Подразумевается, что проект состоит из этапов, на каждом этапе клиенту необходимы определенные типы товаров.
Проект может быть как коротким (например, установить новый смеситель на кухню), так и длительным и сложным (например, перепланировка квартиры).



## Требования
* Python 3.6
* Pytorch 0.4.0
* CUDA >= 8.0

В данном приложении исплоьзуются Deep Autoencoders для создания системы рекоммендаций для клиентов LeroyMerlin.
В данном файле описано, по какому принципу организован API для оболочки автоэнкодэра.
Автоэнгодэр в этом приложении создан с использованием библиотеки [PyTorch](http://pytorch.org/) и основана на репозитории NVIDIA.

Для API мы используем библиотеки:
* [Flask](http://flask.pocoo.org/) - микрофреймворк, созданный на Python, для запуска web приложений
* [CherryPy](https://cherrypy.org/) - минималистичный фреймворк для создания web приложений на Python

## Адаптация модели для Leroy Merlin

О первоначальной модели.
Выбранная модель была создана в 2017 году, и показала очень высокую точность предсказания. Изначально модель создана и протестирована на пользовательских оценках фильмов из базы данных Netflix.

### Товарные категории (модель Адео) вместо конкретных товаров

Основная цель Алгоритма - угадать проект клиента, понять, на какой он стадии, и предложить нужные продукты.
Модель не ставит себе целью понять, какую именно, к примеру, дрель предложить клиенту.
Цель модели - угадать, что конкретному клиенту в данным момент потребоваться дрель, и сократить его путь к данной категории.
Ввиду этого, первым этапом артикулы заменяются на модели Адео, в которых они находятся.

Данный подход, модель Адео вместо конкретного артикула, имеет ряд преимуществ:
* Снижается зависимость от периода обучения. 
Если происходит смена коллекции, и одни дрели заменяются на другие, 
Автоэнкодер всегда работает с одной единицей - моделью Дрели.
* Значительно сокращается количество анализируемых продуктов (со 190тыс до 10тыс), 
благодаря чему в десятки раз повышается точность Автоэнкодера.
* Модель не зависит от того, что в разных городах разные гаммы товаров.
* Модель сможет легко работать с новинками, включая товары лонгтейл и маркетплейс.
* Более простая постобработка рекоммендаций - получаем номер модели, 
накладываем нужные нам фильтры (например, предлагаем только СТМ)
* Ввиду того, что модели Адео международные, есть возможность работать с одним Алгоритмом (как дообучать, так и пользоваться), как в России, так и в других странах, в которых базы данных основаны на Step.

### Проекты имеют жизненный цикл и порядок

Система рекоммендаций для DIY существенно отличается от таковой для FMCG, Фильмов, Музыки. Цель данной модели - улучшить изначальный алгоритм, чтобы учесть следующие факторы.

* Проект клиента - пошаговый процесс. Например, если клиент купил напольное покрытие, то, несмотря на то, что 

