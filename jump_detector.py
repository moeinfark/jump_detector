from binance.client import Client
from binance.enums import *
from decimal import Decimal
import requests
import re
import math
import time

# global variables

boom = u'\U0001F4A5'
biohazard = u'\U00002623'
red_circle = u'\U0001F534'
green_circle = u'\U0001F7E2'
red_cross_mark = u'\U0000274C'
check_mark = u'\U00002714'
check_mark_button = u'\U00002705'
hand_write = u'\U0000270D'
rocket = u'\U0001F680'
interval_global = "4h"
ema_length = 19
ema_factor = Decimal(2) / (ema_length + 1)
usdt_symbols = []
howmuch_map = {}
kafe_symbol = {}
kharid_symbol = {}
symbols = []
step_symbol = {}
price_step = {}
symbolZ = []
valid_list = []
# buy_order_market function should have integer input
each_order_size = 15.00
binance_orders_id = []
binance_map = {}
binance_reverse_map = {}
all_prices = {}
last_price = {}
buy_orders = {}
sell_orders = {}
buy_order_counter = 1
the_last_candle_time = -1
dont_buy = True

def send_message(message_):
    try:
        requests.get('https://api.telegram.org/bot1893930379:AAG1i5MhdCNk6mVqzlTHStoYFob1L_HWNvs/sendMessage?chat_id'
                     '=@asdzxcfvg&text=' + message_)
    except Exception as error:
        print("Telegram api has some problems, in line 12 error is: " + str(error))
        print("bot will go sleep for 60 seconds!")
        time.sleep(60)


def send_message_debug(message_):
    try:
        requests.get('https://api.telegram.org/bot1779177496:AAFZYyMmO77PAwo94dP7Alx6rizH1IZgQxA/sendMessage?chat_id'
                     '=@Tzuilirewev67ibk973cwvthjemcwrg&text=' + message_)
    except Exception as error:
        print("Telegram api has some problems, in line 21 error is: " + str(error))
        print("bot will go sleep for 60 seconds!")
        time.sleep(60)


def send_message_to_control_group(message_):
    try:
        requests.get('https://api.telegram.org/bot1893930379:AAG1i5MhdCNk6mVqzlTHStoYFob1L_HWNvs/sendMessage?chat_id=-1001587793975&text=' + message_)
    except Exception as error:
        print("Telegram api has some problems, in line 21 error is: " + str(error))
        print("bot will go sleep for 60 seconds!")
        time.sleep(60)


def request_to_main_api(request_text):
    while True:
        try:
            response__ = requests.get(request_text)
            return response__
        except Exception as error:
            print("Main api can't response, in line 31 error is: " + str(error))
            print("Bot will go sleep for 60 seconds!")
            time.sleep(60)


send_message_debug("We can do everything that you can think about that!")


api_key = 'UuzQN5OGyU8tTAxuAC5mV6Z18kwDz3Q0s5TrJpEu86fDmIPudhG9i1fy3b3fe98w'
api_secret = 'nYPZUwwVP0D9xlSciIefK8pYAPcIUYHz2BvVxvpbQPEhrWB0haHi84r5f2g7zgN0'

client = Client(api_key, api_secret)

send_message_debug('logged in binance!')

request_global = "https://api.binance.com/api/v3/exchangeInfo"
response_global = requests.get(request_global)
data_global = response_global.json()
stable_coins_list = ["BTGUSDT", "SUSDUSDT", "USDCUSDT", "PAXUSDT", "BUSDUSDT", "TUSDUSDT", "HUSDUSDT", "XAUTUSDT", "QCUSDT",
                     "DAIUSDT", "EURSUSDT", "USDKUSDT", "USDNUSDT", "ANCTUSDT", "GUSDUSDT", "USDQUSDT", "XCHFUSDT",
                     "VNDCUSDT", "BITCNYUSDT", "EBASEUSDT", "USDXUSDT", "EOSDTUSDT", "USNBTUSDT", "CONSTUSDT",
                     "USDSUSDT", "USDHUSDT", "IDRTUSDT", "NUSDUSDT", "SAIUSDT", "XEURUSDT", "BGBPUSDT", "BRZUSDT",
                     "CUSDUSDT", "KRTUSDT", "UPEURUSDT", "UPTUSDT", "UPUSDUSDT", "USDJUSDT", "USDSUSDT", "USDSBUSDT",
                     "EURUSDT", "ERDUSDT"]

for i_global in data_global["symbols"]:
    help_ = i_global["symbol"]
    match = re.match("[A-Z0-9]+UP[A-Z0-9]+", help_)
    up_ = bool(match)
    match = re.match("[A-Z0-9]+DOWN[A-Z0-9]+", help_)
    down_ = bool(match)
    match = re.match("[A-Z0-9]*BEAR[A-Z0-9]+", help_)
    bear_ = bool(match)
    match = re.match("[A-Z0-9]*BULL[A-Z0-9]+", help_)
    bull_ = bool(match)
    # check

    if i_global["quoteAsset"] == "USDT" and not up_ and not down_ and not bear_ and not bull_ and not(help_ in stable_coins_list):
        request = "https://api3.binance.com/api/v3/klines?symbol=" + help_ + "&interval=" + interval_global + "&limit=1000"
        response = request_to_main_api(request)
        data = response.json()
        if len(data) < 14:
            send_message(boom + " " + help_ + " " + boom + " is not valid crypto to analysis because it is new")
        else:
            step_symbol[help_] = float(i_global["filters"][2]["stepSize"])
            price_step[help_] = float(i_global["filters"][0]["minPrice"])
            symbolZ.append(i_global["baseAsset"])
            symbols.append(i_global["symbol"])


def atr(symbol_atr):
    request_atr = "https://api2.binance.com/api/v3/klines?symbol="+symbol_atr+"&interval=" + interval_global + "&limit=1000"
    response_atr = request_to_main_api(request_atr)
    data_atr = response_atr.json()
    # print(data)
    atr_ = Decimal(0.0)
    atr_pre = Decimal(max(Decimal(data_atr[1][2])-Decimal(data_atr[1][3]), Decimal(abs(Decimal(data_atr[1][2])-Decimal(data_atr[1-1][4]))), Decimal(abs(Decimal(data_atr[1][3])-Decimal(data_atr[1-1][4])))))

    for i in range(2, len(data_atr)-1):
        tr = Decimal(max(Decimal(data_atr[i][2])-Decimal(data_atr[i][3]), Decimal(abs(Decimal(data_atr[i][2])-Decimal(data_atr[i-1][4]))), Decimal(abs(Decimal(data_atr[i][3])-Decimal(data_atr[i-1][4])))))
        atr_ = (atr_pre * 13 + tr) / 14
        atr_pre = atr_

    return atr_


def ema(symbol_ema):
    request_ema = "https://api2.binance.com/api/v3/klines?symbol=" + symbol_ema + "&interval=" + interval_global + "&limit=1000"
    # print(request)
    response_ema = request_to_main_api(request_ema)
    data_ema = response_ema.json()
    # print(data)
    ema_ = Decimal(0.0)
    avg = Decimal(0.0)

    for i in range(0, min(ema_length, len(data_ema))):
        avg = avg + Decimal(data_ema[i][4])

    # be careful about len(data) or len(data) - 1
    for i in range(ema_length, len(data_ema)-1):
        ema_ = Decimal(data_ema[i][4]) * ema_factor + ema_ * (1 - ema_factor)

    return float(ema_)


def _helper(price, step):
    step = int(math.log10(1 / float(step)))
    price = math.floor(float(price) * 10 ** step) / 10 ** step
    price = "{:0.0{}f}".format(float(price), step)
    return str(int(price)) if int(step) == 0 else price


def set_sell(symbol_, quantity_, price_):
    quantity_ = _helper(quantity_, step_symbol[symbol_])
    price_ = _helper(price_, price_step[symbol_])
    while True:
        try:
            order_set_sell = client.create_order(
                symbol=symbol_,
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity_,
                price=price_)
            send_message_debug(str(order_set_sell))
            break
        except Exception as error:
            send_message_debug("Oops!  We have problem in set_sell function and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)


def set_buy(symbol_, quantity_, price_):
    quantity_ = _helper(quantity_, step_symbol[symbol_])
    price_ = _helper(price_, price_step[symbol_])
    print(symbol_, quantity_, price_)
    for i in range(2):
        try:
            order_ = client.create_order(
                symbol=symbol_,
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity_,
                price=price_)
            send_message_debug(str(order_))
            return order_['orderId']
        except Exception as error:
            send_message_debug("Oops!  We have problem in set_buy function and bot must sleep for 15 seconds! and error is: " + str(error))
            if i == 0:
                time.sleep(15)
    return -1

# this function is not used in this program yet


def set_buy_market(symbol_, quote_quantity_):
    # quantity_ = _helper(quote_quantity_, step_symbol[symbol_])
    for i in range(2):
        try:
            order_set_buy_market = client.create_order(
                symbol=symbol_,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quoteOrderQty=quote_quantity_
            )
            send_message_debug(str(order_set_buy_market))
            return order_set_buy_market['orderId']
        except Exception as error:
            send_message_debug("Oops!  We have problem in set_buy_market function and bot must sleep for 15 seconds! and error is: " + str(error))
            if i == 0:
                time.sleep(15)
    return -1


def cancel_order(symbol_, order_id):
    while True:
        try:
            result = client.cancel_order(
                symbol=symbol_,
                orderId=order_id)
            return result
        except Exception as error:
            send_message_debug("Oops!  We have problem in cancel_order function and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)


def get_order(symbol_, order_id):
    while True:
        try:
            order_ = client.get_order(
                symbol=symbol_,
                orderId=order_id)
            return order_
        except Exception as error:
            send_message_debug("Oops!  We have problem in get_order function and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)


def get_balance_free(crypto_name):
    while True:
        try:
            balance_ = client.get_asset_balance(asset=crypto_name)
            print(balance_)
            return float(balance_['free'])
        except Exception as error:
            send_message_debug("Oops!  We have problem in get_balance_free function and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)


def update_prices():
    request_update_prices = "https://api3.binance.com/api/v3/ticker/price"
    response_update_prices = request_to_main_api(request_update_prices)
    data_update_prices = response_update_prices.json()
    for i in data_update_prices:
        if i["symbol"] in symbols:
            last_price[i["symbol"]] = float(i["price"])


def get_balance(crypto_name):
    while True:
        try:
            balance_ = client.get_asset_balance(asset=crypto_name)
            print(str(balance_))
            return float(balance_['free']) + float(balance_['locked'])
        except Exception as error:
            send_message_debug("Oops!  We have problem in get_balance function and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)


# -------------------------------------------------------------------


def check_real_buy_orders():
    list_of_remove = []
    for order_should_check in binance_orders_id:
        help_1 = binance_map[order_should_check]
        order__ = get_order(help_1[0], help_1[1])
        if order__['status'] == 'FILLED':
            list_of_remove.append(order_should_check)
            # send_message("order should check:" + str(order_should_check))
            _price = (float(buy_orders[int(order_should_check)][4]) + float(buy_orders[int(order_should_check)][2]) * 4.00) / 5.00
            hmm_ = get_balance_free(help_1[0][:len(help_1[0]) - 4])
            set_sell(help_1[0], hmm_, _price)
            send_message(red_circle + " " + str(help_1[0]) + " is set for sell at: " + str(_price) + "$\nfor " + str((float(_price) / float(buy_orders[int(order_should_check)][2]) - 1.00) * 100) + "% profit")
    # Delete FILLED status orders from real_buy_orders_id list
    for item_that_should_remove in list_of_remove:
        binance_orders_id.remove(item_that_should_remove)
        buy_orders.pop(item_that_should_remove)


def create_real_buy_orders():
    if dont_buy:
        return
    list_for_sort = []
    update_prices()
    for order_ in buy_orders:
        symbol_help = buy_orders[order_][1]
        buy_price = float(buy_orders[order_][2])
        shakhes = (float(last_price[symbol_help]) - buy_price) / buy_price
        list_for_sort.append((shakhes, order_))
    list_for_sort.sort()

    number_of_real_orders = int(float(get_balance('USDT')) / float(each_order_size))

    # This line should delete for start buy and sell again
    # number_of_real_orders = 0

    if number_of_real_orders == 0:
        list_of_remove = []
        for order_ in buy_orders:
            symbol_help = buy_orders[order_][1]
            request_create_real = "https://api2.binance.com/api/v3/klines?symbol=" + symbol_help + "&interval=" + interval_global + "&limit=1"
            response_create_real = request_to_main_api(request_create_real)
            data_create_real = response_create_real.json()
            if float(data_create_real[0][3]) <= buy_orders[order_][2]:
                list_of_remove.append(order_)
                send_message(biohazard)
                send_message(symbol_help + " was deleted from buy orders because we failed buying in entry price!")
        for order_ in list_of_remove:
            buy_orders.pop(order_)

    just_remove_it = []
    for order__ in buy_orders:
        sell_price = (float(buy_orders[order__][4]) + float(buy_orders[order__][2]) * 4.00) / 5.00
        buy_price = float(buy_orders[order__][2])
        if sell_price / buy_price <= 1.002:
            just_remove_it.append(order__)

    for order__ in just_remove_it:
        buy_orders.pop(order__)

    order_id_should_be_in_binance = []

    for i in range(min(number_of_real_orders, len(list_for_sort))):
        order_id_should_be_in_binance.append(list_for_sort[i][1])

    # send_message(str(order_id_should_be_in_binance))

    orders_in_binance = client.get_open_orders()
    for order_ in orders_in_binance:
        if order_['side'] == 'BUY':
            _pair = (order_['symbol'], order_['orderId'])
            _id = binance_reverse_map[_pair]
            if not(_id in order_id_should_be_in_binance):
                cancel_order(order_['symbol'], order_['orderId'])
                send_message(red_cross_mark + " " + str(order_['symbol']) + " buy order is canceled!")
                binance_orders_id.remove(_id)

    update_prices()
    for ii in range(len(order_id_should_be_in_binance)):
        _id = order_id_should_be_in_binance[ii]
        if not(_id in binance_orders_id):
            price_ = float(buy_orders[_id][2])
            # should order
            if float(last_price[buy_orders[_id][1]]) < price_:
                order_id_ = set_buy_market(buy_orders[_id][1], each_order_size)
            else:
                order_id_ = set_buy(buy_orders[_id][1], each_order_size/price_, price_)
            if order_id_ != -1:
                send_message(green_circle + " a buy order is set for " + str(buy_orders[_id][1]) + "at: " + str(price_) + "$")
                binance_map[_id] = (buy_orders[_id][1], order_id_)
                binance_reverse_map[(buy_orders[_id][1], order_id_)] = _id
                binance_orders_id.append(_id)
            else:
                buy_orders.pop(_id)
    # send_message("2")


def orders_update():
    for i in buy_orders:
        request_orders_update = "https://api3.binance.com/api/v3/klines?symbol=" + buy_orders[i][1] + "&interval=" + interval_global + "&limit=4"
        response_orders_update = request_to_main_api(request_orders_update)
        data_2 = response_orders_update.json()

        buy_orders[i] = (buy_orders[i][0], buy_orders[i][1], buy_orders[i][2], buy_orders[i][3], (float(data_2[2][2]) + float(data_2[2][4])) / float(2.00), buy_orders[i][5])

        if buy_orders[i][3] == "high" and buy_orders[i][5] is False and buy_orders[i][0] != str(data_2[3][0]):
            # data[3][0]
            if buy_orders[i][0] != str(data_2[3][0]):
                if float(data_2[1][2]) / float(data_2[2][3]) >= pow(float(data_2[1][2]) / float(data_2[0][4]), 0.5):
                    buy_orders[i] = (str(data_2[3][0]), buy_orders[i][1], buy_orders[i][2], buy_orders[i][3], buy_orders[i][4], True)
                    message_ = "bot accepted buy order of " + buy_orders[i][1] + " in high position"
                    send_message_debug(message_)
                else:
                    buy_orders[i] = (str(data_2[3][0]), buy_orders[i][1], ema(buy_orders[i][1]) + float(price_step[buy_orders[i][1]]), "ema", buy_orders[i][4], True)
                    if i in binance_orders_id:
                        help_1 = binance_map[i]
                        order_should_check = client.get_order(
                            symbol=help_1[0],
                            orderId=help_1[1])
                        if order_should_check['status'] != 'FILLED':
                            cancel_order(help_1[0], help_1[1])
                            price_ = float(buy_orders[i][2])
                            order_id_ = set_buy(buy_orders[i][1], each_order_size / price_, price_)
                            if order_id_ != -1:
                                binance_map[i] = (buy_orders[i][1], order_id_)
                                binance_reverse_map[(buy_orders[i][1], order_id_)] = i
                                message_ = "bot changed buy order of " + buy_orders[i][1] + " from high to EMA"
                                send_message_debug(message_)
                            else:
                                send_message(buy_orders[i][1] + " is deleted from buy_orders due to binance disconnection!")
                                buy_orders.pop(i)
        elif buy_orders[i][3] == "ema" and buy_orders[i][0] != str(data_2[3][0]):
            message_ = "bot updated buy order of " + buy_orders[i][1] + " from old EMA to new EMA"
            send_message_debug(message_)
            # buy_orders[i][2] = ema(buy_orders[i][1])
            buy_orders[i] = (str(data_2[3][0]), buy_orders[i][1], ema(buy_orders[i][1]) + float(price_step[buy_orders[i][1]]), buy_orders[i][3], buy_orders[i][4], buy_orders[i][5])
            if i in binance_orders_id:
                help_3 = binance_map[i]
                order_should_check = client.get_order(
                    symbol=help_3[0],
                    orderId=help_3[1])
                if order_should_check['status'] != 'FILLED':
                    cancel_order(help_3[0], help_3[1])
                    price_ = float(buy_orders[i][2])
                    order_id_ = set_buy(buy_orders[i][1], each_order_size / price_, price_)
                    if order_id_ != -1:
                        binance_map[i] = (buy_orders[i][1], order_id_)
                        binance_reverse_map[(buy_orders[i][1], order_id_)] = i
                    else:
                        send_message(buy_orders[i][1] + " is deleted from buy_orders due to binance disconnection!")
                        buy_orders.pop(i)


# print(get_balance_free("USDT"))


telegram_message_offset = 987615628


def check_orders():
    global telegram_message_offset
    global dont_buy

    request_ = "https://api.telegram.org/bot1893930379:AAG1i5MhdCNk6mVqzlTHStoYFob1L_HWNvs/getUpdates?chat_id=fGzRBdSpH0FlNzlk&offset=" + str(
        telegram_message_offset)
    while True:
        try:
            response_ = requests.get(request_)
            break
        except Exception as error:
            send_message_debug("Oops!  We have problem in check_orders function in line 455 and bot must sleep for 15 seconds! and error is: " + str(error))
            time.sleep(15)
    data_ = response_.json()
    if data_['ok']:
        for _i in data_['result']:
            if 'message' in _i and 'text' in _i['message']:
                print(_i)
                message_ = _i['message']['text']
                message_items = message_.split(" ")
                if message_.lower() == "are you alive?":
                    send_message_to_control_group("Yeah, yeah, don't worry, I am here ad everything is under control!")
                elif message_.lower() == "do buy":
                    dont_buy = False
                    send_message_to_control_group("bot changed position to do buy!")
                elif message_.lower() == "don't buy" or message_.lower() == "dont buy" or message_.lower() == "do not buy":
                    dont_buy = True
                    send_message_to_control_group("bot changed position to don't buy!")
                elif message_items[0].lower() == 'cancelbuy':
                    id_ = int(message_items[1])
                    if id_ in binance_orders_id:
                        pair_needs = binance_map[id_]
                        cancel_order(pair_needs[0], pair_needs[1])
                        binance_orders_id.remove(id_)
                    if id_ in buy_orders:
                        buy_orders.pop(id_)
                    send_message(hand_write + " buy order of " + str(id_) + " canceled!")
                    send_message_to_control_group("Your message received and well done!")
                elif message_items[0].lower() == 'cancelsell':
                    _symbol = str(message_items[1]).upper()
                    orders_in_binance = client.get_open_orders()
                    for helper in orders_in_binance:
                        if helper['symbol'] == _symbol and helper['side'] == 'SELL' and helper['status'] == 'NEW':
                            cancel_order(helper['symbol'], helper['orderId'])
                            send_message(hand_write + " sell order of " + helper['symbol'] + " canceled!")
                            send_message_to_control_group("Your message received and well done!")
                            break
                elif message_items[0].lower() == 'buy':
                    print('buy')
                elif message_items[0].lower() == 'sell':
                    if len(message_items) == 3:
                        _symbol = str(message_items[1]).upper()
                        _price = float(message_items[2])
                        print(_symbol)
                        _quantity = float(get_balance_free(_symbol[:len(_symbol)-4]))
                        set_sell(_symbol, _quantity, _price)
                        send_message(hand_write + " sell set for " + _symbol + "!")
                        send_message_to_control_group("Your message received and well done!")
                    elif len(message_items) == 4:
                        _symbol = str(message_items[1]).upper()
                        _price = float(message_items[2])
                        _quantity = min(float(get_balance_free(_symbol[:len(_symbol)-4])), float(message_items[3]))
                        set_sell(_symbol, _quantity, _price)
                        send_message(hand_write + " sell set for " + _symbol + "!")
                        send_message_to_control_group("Your message received and well done!")
            telegram_message_offset = _i['update_id'] + 1


while True:
    check_orders()
    time.sleep(60)
    check_real_buy_orders()
    create_real_buy_orders()
    check_orders()

    request = "https://api3.binance.com/api/v3/klines?symbol=BTCUSDT&interval=" + interval_global + "&limit=1"
    response = request_to_main_api(request)
    data1 = response.json()

    if the_last_candle_time == -1 or the_last_candle_time != data1[0][0]:
        the_last_candle_time = data1[0][0]
    else:
        continue

    BTC_price_to_usdt = 0.00

    orders_update()
    for symbol in symbols:
        limit = "3"

        request = "https://api3.binance.com/api/v3/klines?symbol=" + symbol + "&interval=" + interval_global + "&limit=" + limit
        response = request_to_main_api(request)
        data = response.json()

        if len(data) < 3:
            continue

        # candle 0
        candle_0_open = data[0][1]
        candle_0_high = data[0][2]
        candle_0_low = data[0][3]
        candle_0_close = data[0][4]
        # candle 1
        candle_1_open = data[1][1]
        candle_1_high = data[1][2]
        candle_1_low = data[1][3]
        candle_1_close = data[1][4]

        if symbol == "BTCUSDT":
            BTC_price_to_usdt = float(data[2][4])

        atr_indicator = atr(symbol)

        if float(candle_1_high) - float(candle_0_close) >= 2 * float(atr_indicator):
            message = "jump in 4h chart of " + symbol
            send_message_debug(message)
            # --------------------------------------------------
            message = "set order for " + symbol
            send_message_debug(message)
            buy_orders[buy_order_counter] = (str(data[2][0]), str(symbol), float(candle_0_high) + float(price_step[symbol]), "high", (float(candle_1_close) + float(candle_1_high)) / float(2.00), False)
            buy_order_counter = buy_order_counter + 1

    send_message_debug(str(buy_orders))

    info = client.get_account_snapshot(type='SPOT')

    btc_quantity = float(info['snapshotVos'][0]['data']['totalAssetOfBtc'])

    Big_message = "Buy orders: \n"
    for order in buy_orders:
        Big_message = Big_message + check_mark_button + " "
        Big_message = Big_message + str(order) + " "
        Big_message = Big_message + str(buy_orders[order][1]) + ", buy price: "
        Big_message = Big_message + str(buy_orders[order][2]) + "\n"
    Big_message = Big_message + rocket + rocket + " total price is: " + str(BTC_price_to_usdt*btc_quantity) + "$ " + rocket + rocket

    send_message(Big_message)
