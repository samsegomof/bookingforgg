import numpy as np
import pywebio

from pywebio.input import TEXT, FLOAT, PASSWORD, DATE, TIME, NUMBER, input_group
from pywebio.output import put_html, put_row, put_button, use_scope, put_buttons, put_markdown, put_text, put_table
import datetime
import pywebio_battery
import time

from functools import partial
import pandas as pd

from booking_bd import *

@pywebio.config(title='Good Game Администратор',
                description='Просмотр, редактирование и изменение бронирований',
                theme='dark')
class Booking_admin():

    def __init__(self):


        login = pywebio.input.input(
            label='Логин',
            name='login'
        )
        password = pywebio.input.input(
            label='Пароль',
            name='password',
            type=PASSWORD
        )

        # admin_login = input_group(
        #     label='Получение доступа к приложению',
        #     inputs=[login, password],
        #     validate=self.Check_login
        # )


        with use_scope('functions'):

            put_html('<h1 align="center"> Панель администратора </h1>')

            put_markdown('## Ручное добавление бронирования')
            put_button(
                label='Добавить бронирование',
                onclick=self.Add_new_booking,
            )

            put_markdown('## Просмотр бронирований')
            pywebio.pin.put_input(
                name='selecting_date',
                type=DATE,
                label='Дата просмотра бронирований',
                value= str(datetime.date.today())
            )
            put_button(
                label='Выбрать дату',
                onclick=self.Show_bookings,
            )



    def Show_bookings(self):

        while True:
            self.selecting_date = pywebio.pin.pin['selecting_date']

            self.selecting_date = pd.to_datetime(f'{self.selecting_date} 00:00')



            pywebio.output.clear('Bookings')
            with use_scope('Bookings'):
                put_html('<h1 align="center"> Просмотр бронирований </h1>')
                put_text(f"База данных обновлена в {datetime.datetime.now().time().strftime('%H:%M:%S')}")

                pywebio.output.put_tabs([
                    {'title': 'PS-5', 'content': self.Outuput_booking(title='PS-5', place=1, date=self.selecting_date)},
                    {'title': 'Xbox X', 'content': self.Outuput_booking(title='Xbox', place=2, date=self.selecting_date)},
                    {'title': 'VR', 'content': self.Outuput_booking(title='VR', place=3, date=self.selecting_date)},
                    {'title': 'Кафе', 'content': self.Outuput_booking(title='Кафе', place=4, date=self.selecting_date)},
                    {'title': 'VIP rooms', 'content': self.Outuput_booking(title='VIP rooms', place=5, date=self.selecting_date)}
                ])

            time.sleep(300)



    def Outuput_booking(self, title, place, date):

        table_columns = ['#', 'Имя', 'Телефон', 'Начало', 'Конец', 'Действия']
        quantity_tables = {
            1: 4,
            2: 1,
            3: 2,
            4: 5,
            5: 2
        }

        put_xxx_list = []

        for table in np.arange(1, quantity_tables[place] + 1):

            results = Select_bookings(
                date=date,
                place=int(place),
                table=int(table)
            )

            put_xxx_list.append(put_markdown(f'## Столик №{table}'))


            if results == []:
                put_xxx_list.append(put_text('Нет бронирований'))
            else:
                table = []
                for id, name, phone_number, start, end in results:
                    table.append([id, name, phone_number, start.strftime('%H:%M'), end.strftime('%H:%M'),
                                  put_row([
                                      put_button('Изменить', onclick=partial(self.Change_booking_popup, id=id), color='warning'),
                                      put_button('Удалить', onclick=partial(self.Delete_booking, id=id), color='danger')
                                  ])])

                put_xxx_list.append(put_table(table, header=table_columns))

        return put_xxx_list



    def Change_booking_popup(self, id):

        slct = Select_booking_by_id(key=id)

        if slct[5] == 1:
            place_name = 'PS-5'
        if slct[5] == 2:
            place_name = 'Xbox X'
        if slct[5] == 3:
            place_name = 'VR(PS4)'
        if slct[5] == 4:
            place_name = 'Столик в кафе'
        if slct[5] == 5:
            place_name = 'VIP-комната'


        name = pywebio.pin.put_input(
            label='Имя',
            type=TEXT,
            name='name',
            value=slct[1]
        )

        phone_number = pywebio.pin.put_input(
            label='Контактный номер телефона',
            type=FLOAT,
            name='phone_number',
            value=slct[2]
        )

        place = pywebio.pin.put_select(
            label='Место бронирования',
            options=['PS-5', 'Xbox X', 'VR(PS4)', 'Столик в кафе', 'VIP-комната'],
            name='place',
            value=place_name
        )

        table = pywebio.pin.put_input(
            label='№ столика',
            type=NUMBER,
            name='table',
            value= slct[6]
        )

        date = pywebio.pin.put_input(
            label='Дата',
            type=pywebio.input.DATE,
            name='date',
            value=str(slct[3].date())
        )

        start_time = pywebio.pin.put_input(
            label='Время бронирования',
            type=TIME,
            name='start_time',
            value=str(slct[3].time())
        )

        booking_hours = pywebio.pin.put_input(
            label='Количество часов бронирования',
            type=NUMBER,
            name='booking_hours',
            value= int((slct[4]-slct[3]).seconds / 3600)

        )


        changing_data = pywebio_battery.popup_input(
            [name, phone_number, place, table, date, start_time, booking_hours],
            title='Изменение бронирования'
        )

        if changing_data != None:
            try:
                if changing_data['place'] == 'PS-5':
                    place = 1
                if changing_data['place'] == 'Xbox X':
                    place = 2
                if changing_data['place'] == 'VR(PS4)':
                    place = 3
                if changing_data['place'] == 'Столик в кафе':
                    place = 4
                if changing_data['place'] == 'VIP-комната':
                    place = 5

                booking_datetime_start = pd.to_datetime(f"{changing_data['date']} {changing_data['start_time']}")
                booking_hours = pd.to_timedelta(changing_data['booking_hours'], 'h')
                booking_datetime_end = booking_datetime_start + booking_hours

                Update_booking(key=id,
                               name=changing_data['name'],
                               phone_number=changing_data['phone_number'],
                               place=int(place),
                               table=int(changing_data['table']),
                               booking_start=booking_datetime_start,
                               booking_end=booking_datetime_end)

                pywebio.output.toast(f'Объявление #{id} успешно отредактировано!')
                self.Show_bookings()
            except:
                pywebio.output.toast(f'Возникла ошибка при добавлении в базу данных')


    def Delete_booking(self, id):

        slct = Select_booking_by_id(key=id)
        table_columns = ['#', 'Имя', 'Телефон', 'Дата', 'Начало', 'Конец']

        confirm = pywebio_battery.confirm('Подтвердите удаление', put_table([[slct[0],
                                                                              slct[1],
                                                                              slct[2],
                                                                              slct[3].strftime('%d/%m/%y'),
                      slct[3].strftime('%H:%M'), slct[4].strftime('%H:%M')]],
                      header=table_columns))

        if confirm == True:
            Delete_booking_bd(key=id)
            pywebio.output.toast(f'Объявление #{id} успешно удалено!')
            self.Show_bookings()


    def Add_new_booking(self):

        name = pywebio.pin.put_input(
            label='Имя',
            type=TEXT,
            name='name'
        )

        phone_number = pywebio.pin.put_input(
            label='Контактный номер телефона',
            type=FLOAT,
            name='phone_number'
        )

        place = pywebio.pin.put_select(
            label='Место бронирования',
            options=['PS-5', 'Xbox X', 'VR(PS4)', 'Столик в кафе', 'VIP-комната'],
            name='place'
        )

        table = pywebio.pin.put_input(
            label='№ столика',
            type=NUMBER,
            name='table'
        )

        date = pywebio.pin.put_input(
            label='Дата',
            type=pywebio.input.DATE,
            name='date'
        )

        start_time = pywebio.pin.put_input(
            label='Время бронирования',
            type=TIME,
            name='start_time'
        )

        booking_hours = pywebio.pin.put_input(
            label='Количество часов бронирования',
            type=NUMBER,
            name='booking_hours'

        )

        data = pywebio_battery.popup_input(
            [name, phone_number, place, table, date, start_time, booking_hours],
            title='Добавление бронирования'
        )

        if data != None:
            try:
                if data['place'] == 'PS-5':
                    place = 1
                if data['place'] == 'Xbox X':
                    place = 2
                if data['place'] == 'VR(PS4)':
                    place = 3
                if data['place'] == 'Столик в кафе':
                    place = 4
                if data['place'] == 'VIP-комната':
                    place = 5

                booking_datetime_start = pd.to_datetime(f"{data['date']} {data['start_time']}")
                booking_hours = pd.to_timedelta(data['booking_hours'], 'h')
                booking_datetime_end = booking_datetime_start + booking_hours

                append_data = {
                    'name': data['name'],
                    'phone_number': str(data['phone_number']),
                    'place': int(place),
                    'table': int(data['table']),
                    'booking_start': booking_datetime_start,
                    'booking_end': booking_datetime_end
                }

                Add_booking(append_data)

                pywebio.output.toast(f'Объявление успешно добавлено!')
                self.Show_bookings()
            except:
                pywebio.output.toast(f'Возникла ошибка при добавлении в базу данных')





    def Check_login(self, data):

        if data['login'] != 'admin':
            return ('login', 'Неправильный логин')
        if data['password'] != '1234':
            return ('password', 'Неправильный пароль')

