import telebot
import requests
import config
import random
import numpy as np
import pandas as pd
from model import BudgetModel

#initialise  bot
bot = telebot.TeleBot(config.BOT_PARAMS['token'])
x = bot.get_me()
print(x)

COMMANDS = "Commands:\n/start - запуск бота\n/help - инфо\n/fit_predict - обучить модель и выдать предсказания\n/feature - значимые параметры модели"
output = None
feature_importance = 91

#handling /commands
@bot.message_handler(commands=['fit_predict'])
def send_welc(message):
    bot.send_message(message.chat.id, 'Секундочку')
    try:
        X = pd.read_csv('features.csv', index_col=0)
        y = pd.read_csv('target.csv', index_col=0)
        inflation = pd.read_csv('inflation.csv', index_col=0)
        print('All of the data has been loaded successfully!')
    except Exception as err:
        print(repr(err))

    y.loc[y.iloc[-1].name + 1, :] = np.nan
    y.loc[y.iloc[-1].name + 1, :] = np.nan
    X = pd.concat([X, inflation['Прогноз (%)']], axis=1)

    model = BudgetModel(X, y, 3)
    predicts = model.predict()
    output = pd.DataFrame({'Год': y.index[-3:],
                           f'{y.columns[0]}': predicts[0],
                           f'{y.columns[1]}': predicts[1]})
    print(output)
    output.to_csv('prediction.csv', index=False, encoding='utf-8-sig')

    feature_importance = model.feature_importances_
    print(1, feature_importance)

    bot.send_message(message.chat.id, 'Модель обучена, держи предсказания')
    bot.send_message(message.chat.id, f"{output.columns.tolist()} \n"
                                      f"{output.iloc[0].values.tolist()[0]} - {int(output.iloc[0].values.tolist()[1])*1000}, {int(output.iloc[0].values.tolist()[2])*1000} \n"
                                      f"{output.iloc[1].values.tolist()[0]} - {int(output.iloc[1].values.tolist()[1])*1000}, {int(output.iloc[1].values.tolist()[2])*1000} \n"
                                      f"{output.iloc[2].values.tolist()[0]} - {int(output.iloc[2].values.tolist()[1])*1000}, {int(output.iloc[2].values.tolist()[2])*1000} \n")

    bot.send_message(message.chat.id, 'Наиболее значимые признаки для прогноза доходов:')
    bot.send_message(message.chat.id, f'{feature_importance[0][1:4]}')

    stick = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, stick)
    #bot.sendDocument(chat_id=message.chat_id,
    #                         document=open('prediction.csv', "r"))

@bot.message_handler(commands=['feature'])
def send_welc(message):
    print(feature_importance)
    if feature_importance == 91:
        bot.send_message(message.chat.id, 'Для начала обучите модель')
    else:
        bot.send_message(message.chat.id, 'Наиболее значимые признаки для прогноза доходов:')
        bot.send_message(message.chat.id, f'{feature_importance}')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, COMMANDS)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome user!")
    bot.send_message(message.chat.id, COMMANDS)


#pool~start the bot
bot.polling()
