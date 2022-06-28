import numpy as np
import pandas
from sqlalchemy import Column, Integer, String, DateTime, create_engine, select, cast, func, desc, asc, delete, update, union_all
from sqlalchemy.orm import declarative_base, relationship, Session
import pandas as pd

Base = declarative_base()


class Booking_bd(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    phone_number = Column(String)
    place = Column(Integer)
    table = Column(Integer)
    booking_start = Column(DateTime)
    booking_end = Column(DateTime)

    def __repr__(self):
        return f"Booking(id={self.id!r}, name={self.name!r}, phone_number={self.phone_number!r}," \
               f"place={self.place!r}, booking_start={self.booking_start!r}, booking_end={self.booking_end!r}"


def Add_booking(data):


    booking = Booking_bd(
        name=data['name'],
        phone_number=data['phone_number'],
        place=data['place'],
        table=int(data['table']),
        booking_start=data['booking_start'],
        booking_end=data['booking_end']
    )

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(booking)
        session.commit()


def Check_vacancy_table(booking_start, booking_end, place):

    quantity_tables = {
        1: 4,
        2: 1,
        3: 2,
        4: 5,
        5: 2
    }

    order_interval = [booking_start, booking_end]

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:

        for table in np.arange(1, quantity_tables[place] + 1):

            delta = pd.to_timedelta('1D')
            yesterday = booking_start - delta
            tomorrow = booking_start + delta

            slct_today = select(Booking_bd.booking_start, Booking_bd.booking_end). \
                where(func.DATE(Booking_bd.booking_start) == booking_start.date()).\
                where(Booking_bd.place == place).\
                where(Booking_bd.table == int(table))

            slct_yesterday = select(Booking_bd.booking_start, Booking_bd.booking_end). \
                where(func.DATE(Booking_bd.booking_start) == yesterday.date()).\
                where(Booking_bd.place == place).\
                where(Booking_bd.table == int(table))

            slct_tomorrow = select(Booking_bd.booking_start, Booking_bd.booking_end). \
                where(func.DATE(Booking_bd.booking_start) == tomorrow.date()). \
                where(Booking_bd.place == place). \
                where(Booking_bd.table == int(table))

            union_slct = union_all(slct_today, slct_yesterday, slct_tomorrow)
            row = session.execute(union_slct).all()

            if row == []:
                vacancy_table = table
                break
            else:
                checking = []
                for booking_interval in row:
                    checking.append(Intersection_TR(order_interval, booking_interval))
                checking = np.array(checking)

                if checking.any() == False:
                    vacancy_table = table
                    break
                else:
                    vacancy_table = None

        return vacancy_table


def Intersection_TR(interval_1, interval_2):
    start_1, end_1 = interval_1
    start_2, end_2 = interval_2

    latest_start = max(start_1, start_2)
    earliest_end = min(end_1, end_2)

    return latest_start < earliest_end


def Select_bookings(date, place, table):

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        slct = select(Booking_bd.id, Booking_bd.name, Booking_bd.phone_number, Booking_bd.booking_start, Booking_bd.booking_end).\
            where(func.DATE(Booking_bd.booking_start) == date.date()).\
            where(Booking_bd.place == place).\
            where(Booking_bd.table == int(table)).\
            order_by(asc(Booking_bd.booking_start)
        )
        row = session.execute(slct).all()

    return row

def Delete_booking_bd(key):

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        dlt = delete(Booking_bd).where(Booking_bd.id == key)
        session.execute(dlt)
        session.commit()

def Select_booking_by_id(key):

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        slct = select(Booking_bd.id, Booking_bd.name, Booking_bd.phone_number, Booking_bd.booking_start, Booking_bd.booking_end,
                      Booking_bd.place, Booking_bd.table).\
            where(Booking_bd.id == key)
        row = session.execute(slct).first()

    return row


def Update_booking(key, name, phone_number, place, table, booking_start, booking_end):

    engine = create_engine("sqlite:////Users/semensemagonov/PycharmProjects/booking_for_gg/database", future=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        upd = update(Booking_bd).where(Booking_bd.id == key).values(
            name=name,
            phone_number=phone_number,
            place=place,
            table=table,
            booking_start=booking_start,
            booking_end=booking_end
        )
        session.execute(upd)
        session.commit()
