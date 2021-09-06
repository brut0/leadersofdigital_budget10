# Проект

### Реализованная функциональность
- проведён анализ данных
- построена модель прогноза доходов полученных от налогов физических лиц и организаций
- разработан протоип сайта принимающий данные по СЭР
- разработан телеграм-бот

### Стек технологий
- flask, docker, python, numpy, pandas, sklearn, catboost, telegram

### Анализ данных в папке notebooks:
- EDA_1.ipynb - первичный анализ данных
- EDA_2.ipynb - углубленный анализ данных (расчёт корреляций)
- extract_features.ipynb - очистка и обработка данных по СЭР
- extract_target.ipynb - очистка и обработка данных по фактическим доходам бюджета
- model.ipynb - построение, анализ и сравнение моделей прогноза
- model-class.ipynb - реализация класса с ансамблем моделей (стэкинг)
(на первом уровне использованы модели Linear, Ridge, ARIMA, CatBoost, а в качестве мета-модели Ridge)

### Исходные тексты src

### Реализация веб сервиса budget
Установка с помощью Docker

### Реализация телеграм бота telegram bot

Демо сервиса доступно по адресу:  
@budgethackersbot (только часть задумки проекта)  



## Команда проекта
Сергей Земсков - analytics, DA, ML  [<img src=https://github.com/png2378/telegram-icon-updater/blob/master/icons/icomute_22_0.png width="16" height="16"/>](https://t.me/sergiozemskov)  
Анастасия Казакова - programming  
Иван Бушуев - analytics, communication  
Кристина Иванова - UX дизайнер  
Юлия Леснова - analytics  
