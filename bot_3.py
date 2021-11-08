import telebot  # импортируем необходимые библиотеки
import requests
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import types
# вводим токен нашего бота
bot = telebot.TeleBot(TOKEN)
# делаем запрос в Беларусбанк о курсах валют
response = requests.get('https://belarusbank.by/api/kursExchange?city=Минск').json()
# из полученного списка словарей берем необходимые значения по ключам
a = response[0]['USD_in']
b = response[0]['USD_out']
c = response[0]['EUR_in']
d = response[0]['EUR_out']
e = response[0]['RUB_in']
f = response[0]['RUB_out']
g = response[0]['UAH_in']
h = response[0]['UAH_out']

@bot.message_handler(commands=['start'])
# создаем кнопки блоков "Погода" и "Курсы валют"
def main(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Погода')
        itembtn2 = types.KeyboardButton('Курсы валют')
        markup.add(itembtn1, itembtn2)
        msg = bot.send_message(message.chat.id, 'Сделайте свой выбор', reply_markup = markup)
        bot.register_next_step_handler(msg, processing)
# обрабатываем сообщения полученные в результате нажатия кнопок
def processing(message):
        if (message.text == 'Погода'):
            city = bot.send_message(message.chat.id, 'Введите название города')
            bot.register_next_step_handler(city, test_1)
        elif (message.text == 'Курсы валют'):
            test_2(message)
# блок "Погода"
def test_1(message):
	# эмоджи
	code_to_smile = {
		"Clear": "\U00002600",
		"Clouds": "\U00002601",
		"Rain": "\U00002614",
		"Drizzle": "\U00002614",
		"Thunderstorm": "\U000026A1",
		"Snow": "\U0001F328",
		"Mist": "\U0001F32B"
	}

	try:
# делаем запрос на сайт openwethermap.com о погоде в городе 'place'
		place = message.text
		config_dict = get_default_config()
		config_dict['language'] = 'ru'

		owm = OWM('b532588fa8f4ac6a3ed59ff44301ac6f', config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather
# получаем необходимые занчения погоды, температуры и т.д.
		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		dt = w.detailed_status
		st = w.status
		pr = w.pressure['press']
		vd = w.visibility_distance
		sr = w.sunrise_time('iso')
		ss = w.sunset_time('iso')
# определяем эмоджи согласно статусу погоды
		if st in code_to_smile:
			wd = code_to_smile[st]
		else:
			wd = "Посмотри в окно, не пойму что там за погода!"
# выводим результат в бот
		bot.send_message(message.chat.id, "В городе " + str(place) + " температура " + str(t1) + " °C" + "\n" +

				"Максимальная температура " + str(t3) + " °C" +"\n" +
				"Минимальная температура " + str(t4) + " °C" + "\n" +
				"Ощущается как " + str(t2) + " °C" + "\n" +
				"Скорость ветра " + str(wi) + " м/с" + "\n" +
				"Давление " + str(pr * 0.750) + " мм.рт.ст" + "\n" +
				"Влажность " + str(humi) + " %" + "\n" +
				"Видимость " + str(vd) + "  метров" + "\n" +
				"Восход " + str(sr) + "\n" +
				"Заход " + str(ss) + "\n" +
				"На данный момент " + str(dt) + "\n" +
				str(wd)
				)

	except:
		bot.send_message(message.chat.id,"Такой город не найден!")

	main(message)
# блок "Курсы валют". Создаем кнопки.
def test_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    itembtn1 = types.KeyboardButton('USD')
    itembtn2 = types.KeyboardButton('EUR')
    itembtn3 = types.KeyboardButton('RUR')
    itembtn4 = types.KeyboardButton('UAH')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id, 'Узнать курс валют банка', reply_markup = markup)
    bot.register_next_step_handler(msg, currency_rate)
# выводим в бот курсы валют
def currency_rate(massage):
			if (massage.text == 'USD'):
				bot.reply_to(massage, f'Доллар США: покупка {a}, продажа {b}')
			elif (massage.text == 'EUR'):
				bot.reply_to(massage, f'Евро: покупка {c}, продажа {d}')
			elif (massage.text == 'RUR'):
				bot.reply_to(massage, f'100 российских рублей: покупка {e}, продажа {f}')
			elif (massage.text == 'UAH'):
				bot.reply_to(massage, f'100 украинских гривен: покупка {g}, продажа {h}')
			main(massage)

bot.polling()