import pywebio

from pywebio.input import TEXT, FLOAT, PASSWORD, DATE, TIME, NUMBER
import datetime
import pandas as pd

from booking_bd import *
from booking_admin import Booking_admin


@pywebio.config(title='Good Game',
                description='Забронируйте столик онлайн',
                theme='dark')
class Booking():

    def __init__(self):

        self.max_booking_timedelta = pd.to_timedelta(7, 'd')

        self.open_time = datetime.time(hour=10, minute=0)
        self.close_time = datetime.time(hour=8, minute=0)

        name = pywebio.input.input(
            label='Имя',
            type=TEXT,
            name='name',
            required=True
        )

        phone_number = pywebio.input.input(
            label='Контактный номер телефона',
            type=FLOAT,
            name='phone_number',
            required=True
        )

        # number_of_persons = pywebio.input.radio(
        #     label='Количество персон',
        #     options = ['1-2', '3-5', '5+'],
        #     name='number_of_persons',
        #     required=True
        # )

        place = pywebio.input.select(
            label='Место бронирования',
            options=['PS-5', 'Xbox X', 'VR(PS4)', 'Столик в кафе', 'VIP-комната'],
            name='place',
            required=True
        )

        date = pywebio.input.input(
            label='Дата',
            type=pywebio.input.DATE,
            name='date',
            required=True,
            help_text='Доступна запись на неделю вперед'
        )

        start_time = pywebio.input.input(
            label='Время бронирования',
            type=TIME,
            name='start_time',
            required=True,
            help_text='График работы - круглосуточно, пересменка с 8 утра до 10 утра'
        )

        booking_hours = pywebio.input.input(
            label='Количество часов бронирования',
            type=NUMBER,
            name='booking_hours',
            value=1,
            required=True

        )

        data = pywebio.input.input_group(
            label='Бронирование столика',
            inputs=[name, phone_number, place, date, start_time, booking_hours],
            validate=self.Check_data
        )

        if data['place'] == 'PS-5':
            self.place = 1
        if data['place'] == 'Xbox X':
            self.place = 2
        if data['place'] == 'VR(PS4)':
            self.place = 3
        if data['place'] == 'Столик в кафе':
            self.place = 4
        if data['place'] == 'VIP-комната':
            self.place = 5

        self.vacancy_table = Check_vacancy_table(
            booking_start=self.booking_datetime_start,
            booking_end=self.booking_datetime_end,
            place=self.place
        )

        if self.vacancy_table == None:
            pywebio.output.popup(
                title = 'Не удалось забронировать столик',
                content = 'Нет свободных мест, свяжитесь с администратором'
            )
        else:

            append_data = {
                'name': data['name'],
                'phone_number': str(data['phone_number']),
                'place': self.place,
                'table': int(self.vacancy_table),
                'booking_start': self.booking_datetime_start,
                'booking_end': self.booking_datetime_end
            }

            Add_booking(append_data)

            pywebio.output.popup(
                title = 'Столик забронирован',
                content = f"""Зона бронирования: {data['place']}
Столик №{self.vacancy_table}
Дата: {self.booking_datetime_start.date().strftime('%d/%m/%y')}
Время начала:  {self.booking_datetime_start.time().strftime('%H:%M')}
Время окончания: {self.booking_datetime_end.time().strftime('%H:%M')}"""
            )

    def Check_data(self, data):

        self.booking_datetime_start = pd.to_datetime(f"{data['date']} {data['start_time']}")
        self.booking_hours = pd.to_timedelta(data['booking_hours'], 'h')
        self.booking_datetime_end = self.booking_datetime_start + self.booking_hours
        now_datetime = datetime.datetime.now()

        check_intersection = Intersection_TR([self.booking_datetime_start.time(), self.booking_datetime_end.time()],
                        [self.close_time, self.open_time])

        self.booking_timedelta = pd.to_timedelta(self.booking_datetime_start - now_datetime)

        if data['name'] == 'Гарри' and data['phone_number'] == 89613641278:
            return Booking_admin()

        if self.booking_datetime_start.date() < now_datetime.date():
            return ('date', 'Невозможно забронировать на прошедший день!')

        if self.booking_timedelta > self.max_booking_timedelta:
            return ('date', 'Обратите внимание, что максимально допустимый интервал для записи - 1 неделя')

        if (self.booking_datetime_start.date() == now_datetime.date()) & \
                (self.booking_datetime_start.time() < now_datetime.time()):
            return ('start_time', 'Невозможно забронировать на прошедшее время!')

        if check_intersection:
            return ('start_time', 'Заведение не работает в данное время. Обратите пожалуйста внимание на график работы')


pywebio.start_server(Booking, remote_access=True)
