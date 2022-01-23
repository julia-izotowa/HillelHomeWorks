
import os
import sqlite3
from typing import List


def connect_to_db():
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cursor = connection.cursor()
    return cursor


def get_unique_first_names() -> List:
    cursor = connect_to_db()
    query = '''
        SELECT Distinct(FirstName)
            FROM customers
    '''
    cursor.execute(query)
    return cursor.fetchall()


def get_profit() -> float:
    cursor = connect_to_db()
    query = '''
        SELECT SUM(UnitPrice * Quantity) 
            FROM invoice_items
    '''
    cursor.execute(query)
    return cursor.fetchall()[0]


if __name__ == '__main__':

    # Получить список уникальных имен
    list_of_unique_first_names = get_unique_first_names()
    print("Количество уникальных имен: ", len(list_of_unique_first_names))
    print("Эти имена: ")
    for name in list_of_unique_first_names:
        print(*name)

    # Получить прибыль
    print("\nПрибыль составила: ", *get_profit())
