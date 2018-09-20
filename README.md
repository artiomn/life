Тестовое задание в "Лабораторию Касперского"
============================================

- [Реализация игры "Жизнь"](#Реализация-игры-Жизнь).
- [Нейронная сеть, предсказывающая ход](#Нейронная-сеть-предсказывающая-ход).


Реализация игры "Жизнь"
-----------------------

![](life.gif)


### Описание

Необходимо, используя подход ООП, разработать интерфейс и реализацию класса, который будет представлять собой состояние игрового поля и контролировать его изменение в соответствии с правилами.
Следует считать, что края игрового поля циклически замкнуты.
[Оригинальное описание в PDF](test_problem_C++.pdf).

**Сейчас реализованы только ходы вперёд и проверка на завершение только по счётчику живых клеток и по количеству изменений на шаге**.


#### Начальные условия игры

- Предполагается, что пользователь имеет замкнутое поле заданного размера.
- На заданном пространстве распределены клетки так, как это задано пользователем.


#### Требования

Исходя из задачи и возможного развития проекта, были выдвинуты следующие требования к движку:

- Пользователь может задавать размер поля.
- Пользователь может задавать распределение на поле.
- Пользователь может контролировать ходы игры, т.е. иметь возможность сделать ход вперёд и ход назад.


### Интерфейс класса

Исходя из требований, класс должен:

- Иметь конструкторы, принимающие распределение в том или ином виде.
- Иметь функции, позволяющие сделать шаги в одном из направлений.
- Быть способен визуализировать поле.


#### Конструкторы

Возможны два конструктора:

- Конструктор, которому передаётся, сформированное пользователем поле.
- Конструктор, которому передаются размеры поля и функция распределения.

Из них я использую только второй, чтобы не привязываться к формату хранения поля.


#### Функция распределения

Считаю, что поле двумерно, потому предполагается, что функции распределения будут передаваться координаты и ссылка на текущий объект класса.
Текущий элемент будет установлен в то значение, которое вернёт функция распределения.


#### Метод хода

- Шаг может передаваться числовым параметром, либо может иметься два метода, позволяющие делать шаги вперёд и назад.
- В качестве интерфейса для реализации хода выбран один метод с целочисленным параметром, как более универсальный.
- Метод возвращает true, если ещё возможны ходы, либо false, если игра завершена.


#### Получение состояния поля

Поле должно быть возвращено обработчику, либо в виде ссылки, либо в виде возможности его обхода через Visitor.

- Был проведён опрос потенциальных пользователей библиотеки (в виде одного разработчика),
  100% пользователей выразили желание работать со ссылкой на поле, а не с Visitor.
- Плюсом же паттерна Visitor будет изоляция метода обработки данных, от структуры хранилища игрового поля.
- Существует компромиссный вариант: считать, что поле всегда двумерно и иметь метод для получения ячейки по заданным координатам.

Было принято решение использовать вариант с методом, возвращающим ячейку по координатам и вариант с Visitor.


### Реализация класса

На текущий момент, для каждой клетки достаточно флага, указывающего чёрная она или белая.
Хранить дополнительные данные не требуется.
Потому, для хранения поля выбран std::vector<bool>.
Преобразование из двумерных координат в одномерные производится "на лету".
Существует внутренний метод, который реализует логику хода.


#### Правила игры

Ход игры:

- В пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь.
- Если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить.
- Если соседей у клетки меньше двух или больше трёх, клетка умирает.

Условия завершения игры:

- На поле не останется ни одной живой клетки.
- Конфигурация на очередном шаге в точности (без сдвигов и поворотов) повторит себя же на одном из более ранних шагов
  (складывается периодическая конфигурация).
- При очередном шаге ни одна из клеток не меняет своего состояния (складывается стабильная конфигурация; предыдущее правило, вырожденное до одного шага назад).


#### Алгоритм работы

Простейший вариант - формировать второй массив, содержащий поле, но он требует двойного расхода памяти.
Чтобы этого избежать, я буду использовать модифицированный алгоритм:

- Состояние клетки зависит только от числа соседей.
- Получаю количество соседей.
- Если клетка меняет своё состояние, заношу её индекс в список изменений.
- Когда все клетки пройдены, применяю список изменений к полю.


### Сборка

Для сборки требуется CMake версии не ниже 3.1 и компилятор, поддерживающий C++14.
Сборка проверялась на gcc. Реализация проверялась на Debian Linux 9.

```
$ cmake . && make
$ ./life 40 30
```


Нейронная сеть, предсказывающая ход
-----------------------------------

### Постановка условия

[По условию задачи](python_life/Task.txt) необходимо создать нейронную сеть, которая сможет предсказывать следующий шаг в игре "Жизнь".
[Данный в задаче генератор](python_life/gol_dataset.py) создаёт массив состояний, в котором каждому случайно сгенерированному состоянию, соответствует состояние, сгенерированное по правилам игры.

Фактически, сеть должна вывести правила игры.
Если знать, что состояние клетки определяется её окрестностью Мура порядка 1, возможно разбить поле на квадраты 3x3 и обучить классификатор на данных квадратах.
В таком случае, задача сводится к задаче классификации при фиксированном числе классов (2^9).

Тем не менее, предполагается, что я этого не знаю. И задача сводится к более общей: "На основе вектора состояния и примеров переходов между векторами, породить следующий вектор состояния".
При этом, "вектор состояния" описывается матрицей поля. И задача является задачей прогнозирования.


### Выбор алгоритма работы и архитектуры сети

Предварительно были исследованы сети прямого распространения.
Сеть подобной конфигурации в Keras на 20 циклах обучения и выборке из 9000 "полей" даёт точность порядка 0.73:

```python
model = Sequential()

model.add(Dense(height, input_shape=(width, height), activation='relu'))
model.add(Dense(width * height, init='uniform', activation='relu'))
model.add(Dense(height, init='uniform', activation='sigmoid'))
model.summary()
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
...

model.fit(x_train, y_train, epochs=20, verbose=1, validation_split=0.1)
```

Проблема в том, что это не 0.75 верно предсказанных результатов, а 0.73 поверхности поля.
Максимум, которого удалось достичь - 0.8 при следующей конфигурации сети:

```python
model.add(Dense(height, input_shape=(width, height), activation='selu'))
model.add(Dense(width * height, init='uniform', activation='relu'))
model.add(Dense(width * height * 10, init='uniform', activation='relu'))
model.add(Dense(height, init='uniform', activation='sigmoid'))
```

Этого явно недостаточно для уверенного предсказания хода на поле размерностью 20x30.

С задачей прогнозирования лучше всего справляются сети с памятью, т.е. рекуррентные.
Если бы переходы из состояния в состояние представляли собой серии событий, то рекуррентные модули, сохраняющие состояние в течение длительного периода, подошли бы лучше всего.
Например, [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) или [GRU](https://en.wikipedia.org/wiki/Gated_recurrent_unit) блоки.

Проблема заключается в том, что генератор создаёт не связанные между собой состояния, а лишь набор независимых переходов: предыдущее состояние - следующее состояние.
Т.е., предыдущее состояние не учитывается.
Если использовать такой рекуррентный модуль, он будет считать, что все сэмплы связаны и запоминать переходы, которые таковыми не являются и не соответствуют правилам.

Один из вариантов - предварительная группировка состояний с целью поиска последовательностей переходов и дальнейшее использование RNN.

Тем не менее, не хочется делать предобработку, основываясь на дополнительном знании о данных (например, о распределении ГСЧ).
Таких последовательностей может не быть. И при возрастании размерности поля, вероятность их обнаружить уменьшается нелинейно.

Однако, Keras содержит [SimpleRNN блок](https://keras.io/layers/recurrent/#simplernn), "проблемой" которого является то, что он забывает ранние состояния.

С таким блоком удалось достигнуть максимальной точности прогноза более 0.97, при использовании враппера [Bidirectional](https://keras.io/layers/wrappers/#bidirectional)


### Реализация

Параметры поля не указываются, а берутся из переданного HDF файла.


### Запуск

`./neuro_life.py dataset_20x30x1000.h5`
