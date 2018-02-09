#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Provides a connection to the compound database

"""

import sys
import sqlite3
import entry


DATABASE = '<path-to-database>'
DATABASE = '/Users/anna/PycharmProjects/tts/dictionary.db'

SQL_SELECT = 'SELECT * FROM compound WHERE word = ?'


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)


def get_compound(wordform, conn):
    result = conn.execute(SQL_SELECT, (wordform,))
    compound = result.fetchone()
    if compound:
        return compound[1], compound[2], compound[3]


def open_connection():
    return create_connection(DATABASE)


