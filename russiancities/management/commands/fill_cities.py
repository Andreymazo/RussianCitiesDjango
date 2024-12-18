from django.core.management import BaseCommand
import psycopg2
import os, csv
import shutil
import time
from django.contrib.gis.geos import Point

from django.core.management import BaseCommand

from russiancities.models import RusCity
from tqdm import tqdm


# russiancities_city
# https://magicstack.github.io/asyncpg/current/usage.html

def ff():
        filename = "cities2.csv"
        # connection establishment
        conn = psycopg2.connect(
            database="russiancitiesdjango",
            user='postgres',
            password='123456',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        #Курсор нужен, чтобы исполнять разные команды в базе например удаление таблицы такой-то и не надо входить в постгрес (50б55 строчки)
        cursor = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            data = csv.reader(f, delimiter=',')
            # d = next(data)
            # print('-------------------')
            for i in tqdm(data, desc="Loading..."):
                *first, a,b = i
                if len(i)==3:
                    RusCity.objects.create(name=i[0], location=Point(float(i[1]), float(i[2])))
                else:
                    RusCity.objects.create(name=''.join(first), location=Point(float(a), float(b)))


           
            # for i in data:  ##Zapoliaem suppliers
            #     cursor.execute(
            # 'INSERT INTO cargo_locations( "zip", "latitude", "longtitude", "city", "state") VALUES (%s, %s, %s, %s, %s)',
            # (i[0], i[1], i[2], i[3], i[5].split(',')[0]))
        #query to create a table
        # sql = '''drop table locations'''
        # sql = ''' CREATE TABLE cargo_locations (zip INT, latitude FLOAT, longtitude FLOAT, city VARCHAR(50), state VARCHAR(50)); '''
        # sql = '''truncate table russiancities_ruscity restart identity cascade'''
        # russiancities_ruscity
        # # # sql = '''COPY cargo_locations FROM '/home/andrey_mazo/PycharmProjects/DjangoProjectCargoTest/cargo/templates/tmp/uszips.csv' WITH (FORMAT csv);'''
        # # # sql = '''COPY cargo_locations FROM '/home/andrey_mazo/PycharmProjects/DjangoProjectCargoTest/cargo/templates/tmp/uszips.csv' DELIMITER ',' CSV HEADER;'''
        # # # sql = \copy cargo_locations FROM '/path/to/csv/ZIP_CODES.txt' DELIMITER ',' CSV
        # cursor.execute(sql)
        # print(len(RusCity.objects.all()))

# ['Ostanovochnyy  ', 'Punkt  ', 'Brusnichnoye  ', 'Brusnichnoe  ', 'Ostanovochnyj  ', 'Брусничное  ', 'Остановочный  ', 'Пункт  ']
# Ostanovochnyy  Punkt  Brusnichnoye  Brusnichnoe  Ostanovochnyj  Брусничное  Остановочный  Пункт  
class Command(BaseCommand):

    def handle(self, *args, **options):
        ff()
      