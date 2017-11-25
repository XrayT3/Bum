import os
import sqlite3
import telebot
import time
import random
from telebot import types
import urllib.request as urllib

import requests.exceptions as r_exceptions
from requests import ConnectionError

import const, base, markups, temp, config

bot = telebot.TeleBot(const.token)
uploaded_items = {}


# ��������� /start ������� - ��������� ������������� �� ���������� � ��������
@bot.message_handler(commands=['start'])
def start(message):
    base.add_user(message)
    if base.is_seller(message.from_user.id):
        bot.send_message(message.chat.id, const.welcome_celler, reply_markup=markups.start())
    else:
        bot.send_message(message.chat.id, const.welcome_client, reply_markup=markups.start1())


# ������ ���� � ������ �������
@bot.message_handler(regexp='����')
def client_panel(message):
    bot.send_message(message.chat.id, '�������� ���������:', reply_markup=markups.show_types(message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data == 'client_panel')
def client_panel(call):
    bot.edit_message_text(const.welcome_client, chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id, text='...', reply_markup=markups.start1())

# ������ ����������� ���������
@bot.callback_query_handler(func=lambda call: call.data == 'celler_panel')
def celler_panel(call):
    bot.edit_message_text('�������. ������ ��������.', call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown', reply_markup=markups.edit())


# ������� � ���������
def hello(message):
    if message.text != '������� �����' and message.text != '������' and message.text != '���������' and message.text != '����� ���������' and message.text != '��� ��������':
        a = random.randint(50, 100)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row('��������', '���������')
        keyboard.row('������', '�����')
        bot.send_message(message.chat.id,
                             '� ������ {name} ������� '.format(name=message.text) + str(a) + ' �����������.')
        print(message.text)
        bot.send_message(message.chat.id, '�������� ������ ���������.', reply_markup=markups.show_types(message.chat.id))


# ����������� ������� � ��������� �� � ���
@bot.callback_query_handler(func=lambda call: call.data in base.give_menu())
def show_items(call):
    for item in base.type_finder(call.data):
        key = item.get_desc2()
        uploaded_items[str(item.id)] = 0
        print(uploaded_items)
        try:
            url = item.url
            photo = open("temp.jpg", 'w')  # ������������� �����
            photo.close()
            photo = open("temp.jpg", 'rb')
            urllib.urlretrieve(url, "temp.jpg")
            bot.send_photo(chat_id=call.message.chat.id, photo=photo)
            bot.send_message(call.message.chat.id, item.description, reply_markup=key)
            photo.close()
            os.remove("temp.jpg")
        except Exception:
                bot.send_message(call.message.chat.id, item.description, reply_markup=key)


# ��������� ������ ������� ������
@bot.callback_query_handler(func=lambda call: call.data in uploaded_items)
def callback_handler(call):
    uploaded_items[str(call.data)] += 1
    print('uploaded_items : ' + str(uploaded_items))
    print('callback_handler.call.data = ' + str(call.data))
    markup = markups.add(call.data)
    a = random.randint(50000, 100000)
    bot.send_message(chat_id=call.message.chat.id,
                          text='��� ������ ����� ������� ��������� �� 30 �����: 1ae085ae-667c'.format(chat_id=call.message.chat.id) + str(a) + '-4155-bb9e-e84c6a7053c'.format(chat_id=call.message.chat.id) + str(a) + '4\n'
                          '�� �������� ��� ���������� � ������ �����  ����� ������.\n'
                          '--------------------------------\n'
                          '������ � ������� QIWI ��� BTC.\n'
                          '!!!����� � ����� ������ ������� � �������� ������� ��� ������!!!\n'
                          '--------------------------------\n'
                          '��������! ������ �� QIWI ������� ������ ������������� c ������������ ������������!\n'
                          '--------------------------------\n'
                          '��������� ��� ������ QIWI:\n'
                          '����� ��������: +79619144459\n'
                          '� ����������� � ������� ������� ����� ������ � ��� ��� Telegram (578040 @helpramp). ����� ��������� ������� ��� ����� �� ����� ����� �����.\n'
                          '������ ����� ���������� ����� ���������� QIWI ��� ������ ���������� �������� ��� ����� ����� �������� QIWI.\n'
                          '--------------------------------\n'
                          '��������� ��� ������ BTC:\n'
                          '��� ������ ����� �������� BTC:  1EcDBmsqAqu3o7vypcZYMn4wZtATswTcTG\n'
                          '����� ��������� 1 ������������� �����, ��� ������� � ��� ����� ������. ������� ��� � ������� 578040. ����� ����� ��� ����� �� ����� ����� �����.\n'
                          '--------------------------------\n'
                          '����� ������� ������ ���� �����, ����� ������� ���������. � ��������� ������ ��� ������ �� ����� �������� � ��������������� ������.\n'
                          '����� �������� ����������������� ����� � ������� ���������� �������, ����� ��� ����� ����� ������. ����� ���� ������� ����� ��������� � �����, ������� ��������� ��� �������� ������ ��� �� ���-����.\n'
                          '����� ��������� ������ �� ������ �������� ����� � ������ ��� �������� �� ����� http://ramp24vqtden6hep.onion/number ��� ������� � ������ ��������� @helpramp, ������ ������  ����� ������� ���������.\n'
                          '��� ������������� �� ������ �������� ������ ���������, ����� ������ "������"', parse_mode='HTML', reply_markup=markup)


# ����� "�������" �� ������ �� ������
@bot.callback_query_handler(func=lambda call: str(call.data[0]) == '+')
def handle_plus(call):
    bot.send_message(chat_id=call.message.chat.id, text='�� ������� ������������� ������, ����������, ��������� ������� ����� ������.\n'
    '���� � ��� �������� ��������, �� ������ �������� � ������ ��������� @helpramp.')


# ����� "���" �� ������ �� ������
@bot.callback_query_handler(func=lambda call: str(call.data[0]) == '-')
def handle_minus(call):
    bot.send_message(chat_id=call.message.chat.id, text='�������� ���������:',
                     reply_markup=markups.show_types(call.message.chat.id))


# ������ ���� �������----------------------------------------


# ���������� ���������
@bot.callback_query_handler(func=lambda call: call.data == 'add_kat')
def handle_add_kat(call):
    sent = bot.send_message(call.message.chat.id, "������� �������� ���������", reply_markup=markups.return_to_menu())
    bot.register_next_step_handler(sent, base.add_kat)


# �������� ���������
@bot.callback_query_handler(func=lambda call: call.data == 'delete_kat')
def handle_delete_kat(call):
    bot.edit_message_text("�������� ��������� ��� ��������", call.message.chat.id,
                          call.message.message_id, reply_markup=markups.delete_kat())


@bot.callback_query_handler(func=lambda call: call.data[0] == '?')
def handle_delete_this_kat(call):
    db = sqlite3.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("DELETE FROM categories WHERE name = ?", (str(call.data[1:]),))
    db.commit()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_kat())
    print('deleted')


# ���������� ������.


# ����� ���� ������
@bot.callback_query_handler(func=lambda call: call.data == 'add_item')
def handle_add_item_type(call):
    new_item = temp.Item()
    const.new_items_user_adding.update([(call.message.chat.id, new_item)])
    sent = bot.send_message(call.message.chat.id, "�������� ��� ������:", reply_markup=markups.add_item())
    bot.register_next_step_handler(sent, base.add_item_kategory)
    const.user_adding_item_step.update([(call.message.chat.id, "Enter name")])


# ���� ������������ ������
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "Enter name")
def handle_add_item_description(message):
    sent = bot.send_message(message.chat.id, "������� ��������")
    bot.register_next_step_handler(sent, base.add_item_description)
    const.user_adding_item_step[message.chat.id] = "End"


# ����� ���������� ������
@bot.message_handler(func=lambda message: base.get_user_step(message.chat.id) == "End")
def handle_add_item_end(message):
    bot.send_message(message.chat.id, "���������!\n ����:", reply_markup=markups.show_types(message.chat.id))
    const.user_adding_item_step.pop(message.chat.id)


# �������� ������
@bot.callback_query_handler(func=lambda call: call.data == 'delete_item')
def handle_delete_item(call):
    bot.edit_message_text("�������� ����� ��� ��������", call.message.chat.id, call.message.message_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_item(call.message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data[0] == '^')
def handle_delete_from_db(call):
    db = sqlite3.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("DELETE FROM items WHERE id = ?", (str(call.data[1:]),))
    db.commit()
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=markups.delete_item(call.message.chat.id))
    print('deleted')


@bot.message_handler(content_types=['text'])
def bank(message):
        markup_start = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup_start.row('��� ��������', '������� �����')
        markup_start.row('������', '���������')
        markup_start.row('����� ���������')
        keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard1.row('������� �����', '������')
        keyboard1.row('���������', '����� ���������')
        keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard3.row('��� ��������', '������� �����')
        keyboard3.row('���������', '����� ���������')
        keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard4.row('��� ��������', '������� �����')
        keyboard4.row('������', '����� ���������')
        keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard5.row('��� ��������', '������� �����')
        keyboard5.row('������', '���������')
        markup_oplata = types.InlineKeyboardMarkup()
        markup_oplata.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['������']])
        if message.text == '��� ��������':
            print('��� ��������')
            bot.send_message(message.chat.id, '������ ��������� ���������������, ������� ������� �� ������� �� ��������� ����� ���������� �� ����� 1 ����.\n'
            '��� ���������� ������ ��� ���������� ������� � ������ "������� �����", ������� ��� ����� � ��� ������������� ������ ��������� �� ����� �������� � ����� ������ � ������� ����� ��������� � �������.\n'
            '����� ������ ������ ��� ����� ������������� ������ ��������� ��� ������. ���� �������� ������������ 2 ������� ������: Qiwi � Btc, ������ �������� ���������� ���� ���������, ������� ��������� ������ ����� ����� ������ ������ �� Qiwi ��� ������ �� Btc.\n'
            '��� ������ �� ���� Qiwi, � ����������� � ������� ����������� ���������� ��� ��� � Telegram � ������� @helpramp. � ��������� ������ ������ �� ����� �������� � �������������� ������.\n'
            '��� ������ Btc, ���������� ��� ����� Btc �������� ������������� � ������ ���� � Telegram, ����� ��������� 1 ������������� ��� ������������� ���������� ����������� ������� � ������� ��� ����� ������. ������� ��� � ������� 578040.\n'
            '����� ���������� �������� ������� �� ������ "� �������", ��� ������������� �������� ��� ������ � ������ ��� ����� ����� �� ���� �������������� ����������� (������� �� �������� � ��� ���������).\n'
            '�� ������ �������� ����� � ������ ��� �������� �� ����� http://ramp24vqtden6hep.onion/number ��� ������� � ������ ��������� @helpramp, ������ ������  ����� ������� ���������.', parse_mode='HTML', reply_markup=keyboard1)
        if message.text == '������':
            print('������')
            bot.send_message(message.chat.id, '�� ������ ����� ��� ����������� ���������� � ������ ��������������� ���� �� �������:\n'
            'http://ramp24vqtden6hep.onion/info\n'
            'http://lkncc.cc/newrampbot\n'
            'http://leomarketjdridoo.onion/newrampbot\n'
            'http://eeyovrly7charuku.onion/newrampbot\n'
            'http://tochka3evjl3sxdv.onion/newrampbot\n'
            '��� �� �� ������ ��������� ������ � ������ ��� �������� �� ����� http://ramp24vqtden6hep.onion/number, ������ ������  ����� ������� ���������.', parse_mode='HTML', reply_markup=keyboard3)
        if message.text == '���������':
            print('���������')
            bot.send_message(message.chat.id, '���� � ��� �������� ���������, �������� � ������� ��� ���������� �����, ��� � ��� ���� ������� � ������ ����- �� ������ ��������� �� ������� ��������� @Newrampbot � Telegram @helpramp.', parse_mode='HTML', reply_markup=keyboard4)
        if message.text == '����� ���������': #� ���� ������ ����� ��������� ���� � �����
            print('����� ���������')
            bot.send_message(message.chat.id, '��� ����, ����� ����� ��������� �� ����� ��������, ��� ���������� ���������� �������� ��� ����������� ����� ��������.\n'
            '��������� �����������:\n'
                '5000 ������ � ����� � ������������ ��������� ������ �� ������������;\n'
                '50000 ������ - ����������� ����� ��������.\n'
                '� ��� ��������� ��������:\n'
                    '������� �����-������ � ������������ ����������� ������ � ������������ (������ � WEB ������), ��������� ���� ��������� � ������� ������ �������� ����� �� ����������� Telegram.\n'
                    '��������� ��������� 24/7.\n'
                    '������� �������������� ��������, ������ �� ����� ������������ ������ �� ���� ����� ��� ��������.\n'
                    '��� ����������� ������ �������� ���������� ��������� ������� �� ��� ���� Qiwi �������� +79619218391 � ��������� ����������� � ������� ������ ���� � Telegram � ������� @helpramp.\n'
                    '����� ���������� ������� � ���� �������� ��� ����� ����������� ���������.', parse_mode='HTML', reply_markup=keyboard5)
        if message.text == '������� �����':
            print('������� �����')
            sent = bot.send_message(message.chat.id, '������� ��� ����� � ������� #�����')
            bot.register_next_step_handler(sent, hello)
        if message.text == '�����':
            print('�����')
            bot.send_message(message.chat.id, '�������� ������.', parse_mode='HTML', reply_markup=markup_start)


# ������ ����
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except ConnectionError as expt:
        config.log(Exception='HTTP_CONNECTION_ERROR', text=expt)
        print('Connection lost..')
        time.sleep(30)
        continue
    except r_exceptions.Timeout as exptn:
        config.log(Exception='HTTP_REQUEST_TIMEOUT_ERROR', text=exptn)
        time.sleep(5)
        continue
