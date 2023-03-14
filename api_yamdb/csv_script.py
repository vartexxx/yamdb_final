import csv
import fnmatch
import os
import sqlite3

DEFAULT_FOLDER = os.path.abspath(os.curdir)
DATABASE_DEFAULT_FOLDER = 'api_yamdb/static/data'
DATABASE_FOLDER = os.path.join(DEFAULT_FOLDER, DATABASE_DEFAULT_FOLDER)
DATABASE_DEFAULT_PATCH_FOLDER = 'api_yamdb'
DBNAME = 'db.sqlite3'
DATABASE_PATCH_FOLDER = os.path.join(DATABASE_DEFAULT_PATCH_FOLDER, DBNAME)

result = []
for root, dirs, files in os.walk(DATABASE_FOLDER):
    for name in files:
        if fnmatch.fnmatch(name, '*.csv'):
            result.append(os.path.join(root, name))
csv_files = result
con = sqlite3.connect(DATABASE_PATCH_FOLDER)
cur = con.cursor()
for element in csv_files:
    with open(element, 'r') as dir:
        dict = csv.DictReader(dir)
        TABLE_NAME = os.path.splitext(os.path.basename(element))[0]
        colums = dict.fieldnames
        num_colums = len(colums)
        to_db = [tuple(i.values()) for i in dict]
        colums_string = ','.join(colums)
        marks = ["?"] * num_colums
        add = ','.join(marks)
        cur.execute(f'CREATE TABLE {TABLE_NAME} ({colums_string});')
        cur.executemany(
            f'INSERT INTO {TABLE_NAME} ({colums_string}) VALUES ({add});',
            to_db
        )
        con.commit()
con.close()
