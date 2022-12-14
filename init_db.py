import os
import psycopg2
from flask_bcrypt import Bcrypt

bcript = Bcrypt()
conn = psycopg2.connect(
        host="dpg-ce0ann1a6gdsa60lpc20-a.frankfurt-postgres.render.com",
        database="wis2",
        user="miguel",
        password="F8tZ8MKi3KB4gJko95puK6EB4VOPaB9s")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users CASCADE;')
cur.execute('DROP TABLE IF EXISTS courses CASCADE;')
cur.execute('DROP TABLE IF EXISTS termin CASCADE;')
cur.execute('DROP TABLE IF EXISTS terminy CASCADE;')
cur.execute('DROP TABLE IF EXISTS course_type CASCADE;')
cur.execute('DROP TABLE IF EXISTS room CASCADE;')
cur.execute('DROP TABLE IF EXISTS lectors CASCADE;')
cur.execute('DROP TABLE IF EXISTS students CASCADE;')
cur.execute('DROP TABLE IF EXISTS termin_type CASCADE;')
cur.execute('DROP TABLE IF EXISTS hodnotenie_studenta CASCADE;')


cur.execute('CREATE TABLE users (login varchar (8) NOT NULL PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'adress varchar (150) NOT NULL,'
                                 'enrollment_date date NOT NULL,'
                                 'password TEXT NOT NULL);'
                                 )

cur.execute('CREATE TABLE course_type (id varchar (50) PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE courses (name varchar (50) NOT NULL PRIMARY KEY,'
                                 'login varchar (8) REFERENCES users (login),'
                                 'type varchar (50) REFERENCES course_type (id),'
                                 'description varchar (250),'
                                 'accepted BOOLEAN NOT NULL,'
                                 'price varchar (250),'
                                 'news varchar (250) );'
                                 )

cur.execute('CREATE TABLE room (id varchar (50) PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE termin_type (id varchar (50) PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE termin (id SERIAL PRIMARY KEY,'
                                 'type varchar (50) REFERENCES termin_type (id),'
                                 'room varchar (50) REFERENCES room (id),'
                                 'name varchar (50) NOT NULL,'
                                 'description varchar (250),'
                                 'date date NOT NULL);'
                                 )

cur.execute('CREATE TABLE lectors (id_course varchar (50) REFERENCES courses (name),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'PRIMARY KEY(id_course, id_users));'
                                 )
cur.execute('CREATE TABLE terminy (id_course varchar (50) REFERENCES courses (name),'
                                 'id_termin int REFERENCES termin (id),'
                                 'PRIMARY KEY(id_course, id_termin));'
                                 )
cur.execute('CREATE TABLE students (id_course varchar (50) REFERENCES courses (name),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'accepted BOOLEAN NOT NULL,'
                                 'PRIMARY KEY(id_course, id_users));'
                                 )
cur.execute('CREATE TABLE hodnotenie_studenta (id_termin int REFERENCES termin (id),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'grade int,'
                                 'PRIMARY KEY(id_termin, id_users));'
                                 )
# Insert data into the table


heslo = bcript.generate_password_hash('chorizo')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('xsanch00',
             'Miguel Sanches',
             'Ulica De la Cruise numero seis, Madrid, Espanol',
             '2019-09-14',
             heslo.decode('utf8')
             )
            )
heslo = bcript.generate_password_hash('tank')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('xszlot01',
             'Jocko Szlota', # Another great classic!
             'Ulica Andreja Hlinku 420, Zilina, 96885, Slotovisko',
             '2012-08-31',
              heslo.decode('utf8')
            )
)
heslo = bcript.generate_password_hash('1111')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('admin',
             'Ignac Vsetkovie',
             'Ulica Kukucinova 12, Vychodne, 98458, Slovensko',
             '1999-08-31',
             heslo.decode('utf8')
             )
            )

cur.execute('INSERT INTO course_type (id,name)'
            'VALUES(\'prezen??ne\',\'prezen??ne\')'
            )
cur.execute('INSERT INTO course_type (id,name)'
            'VALUES(\'distan??ne\',\'distan??ne\')'
            )
cur.execute('INSERT INTO termin_type (id,name)'
            'VALUES(\'Zavere??n?? sk????ka\',\'Zavere??n?? sk????ka\')'
            )
cur.execute('INSERT INTO courses (name, login, type, description, accepted, price)'
            'VALUES (%s, %s, %s, %s,%s,%s)',
            ('IAS',
             'admin',
             'distan??ne',
             'Spr??va informa??n??ho syst??mu',
             'TRUE',
             'Zadarmo'
             )
            )
cur.execute('INSERT INTO lectors (id_course, id_users)'
            'VALUES (%s, %s)',
            ('IAS',
             'admin'
             )
            )
cur.execute('INSERT INTO courses (name, login, type, description, accepted, price)'
            'VALUES (%s, %s, %s, %s,%s,%s)',
            ('IIS',
             'xsanch00',
             'prezen??ne',
             'Tvorenie informacn??ho syst??mu',
             'TRUE',
             'Zadarmo'
             )
            )
cur.execute('INSERT INTO lectors (id_course, id_users)'
            'VALUES (%s, %s)',
            ('IIS',
             'xsanch00'
             )
            )
cur.execute('INSERT INTO room (id,name)'
            'VALUES(\'D105\',\'D105\')'
            )

cur.execute('INSERT INTO room (id,name)'
            'VALUES(\'D215\',\'D215\')'
            )
cur.execute('INSERT INTO room (id,name)'
            'VALUES(\'L101\',\'L101\')'
            )

cur.execute('INSERT INTO termin_type (id,name)'
            'VALUES(\'Dom??ca uloha\',\'Dom??ca uloha\')'
            )
cur.execute('INSERT INTO termin_type (id,name)'
            'VALUES(\'Projekt\',\'Projekt\')'
            )
cur.execute('INSERT INTO termin_type (id,name)'
            'VALUES(\'Polsemestr??lny test\',\'Polsemestr??lny test\')'
            )
cur.execute('INSERT INTO termin (type, room, name, description, date)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('Polsemestr??lny test',
             'D105',
             'Polsemestr??lny test',
             'Test z prv??ch 3 l??tok predmetu',
             '2022-12-12'
             )
            )
cur.execute('INSERT INTO termin (type, room, name, description, date)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('Polsemestr??lny test',
             'L101',
             'Polsemestr??lny test 2. skupina',
             'Test z prv??ch 3 l??tok predmetu',
             '2022-12-12'
             )
            )
cur.execute('INSERT INTO termin (type, room, name, description, date)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('Zavere??n?? sk????ka',
             'L101', # Another great classic!
             '1. term??n',
             'Zavere??n?? sk????ka z predmetu IIS',
             '2022-12-11'
             )
            )
cur.execute('INSERT INTO lectors (id_course, id_users)'
            'VALUES (%s, %s)',
            ('IAS',
             'xsanch00'
             )
            )
cur.execute('INSERT INTO terminy (id_course, id_termin)'
            'VALUES (%s, %s)',
            ('IAS',
             '1'
             )
            )
cur.execute('INSERT INTO terminy (id_course, id_termin)'
            'VALUES (%s, %s)',
            ('IAS',
             '2'
             )
            ) 
cur.execute('INSERT INTO terminy (id_course, id_termin)'
            'VALUES (%s, %s)',
            ('IIS',
             '3' # Another great classic!
             )
            )             
conn.commit()

cur.close()
conn.close()