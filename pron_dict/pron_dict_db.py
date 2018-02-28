

import sys
import sqlite3

MOD = 'modifier'
BASE = 'base'

DATABASE = '/Users/anna/PycharmProjects/tts/dictionary.db'

SQL_CREATE = 'CREATE TABLE IF NOT EXISTS frob(id INTEGER PRIMARY KEY, word TEXT, ' \
                     'transcript TEXT) '

SQL_INSERT = 'INSERT OR IGNORE INTO frob(word, transcript) VALUES(?, ?)'


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def populate_database(dict_list):
    db = create_connection(DATABASE)
    db.execute(SQL_CREATE)
    for entry in dict_list:
        db.execute(SQL_INSERT, (entry[0], entry[1]))

    db.commit()


def main():

    frob = sys.argv[1]

    frob_list = []
    for line in open(frob).readlines():
        word, transcr = line.split('\t')
        frob_list.append([word, transcr.strip()])

    populate_database(frob_list)


if __name__ == '__main__':
    main()
