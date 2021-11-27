import csv
import sqlite3


def dict_factory(cursor, row) -> dict:
    """Генератор строк-словарей для sqlite3"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def trip(max_distance: int, counties: list):
    connection = sqlite3.connect('fjords.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()

    # id, name, country_id, coast_length, depth, water_temperature
    query = """
    SELECT * FROM Fjords 
    INNER JOIN States ON Fjords.country_id = States.id
    WHERE coast_length <= ?"""

    result = cursor.execute(query, (max_distance,)).fetchall()

    result = list(filter(
        lambda x: x['state'] in counties,
        result
    ))

    data = list(map(
        lambda x: {
            'fjord': x['name'],
            'coast_length': x['coast_length'],
            'depth': x['depth'],
            'temperature': x['water_temperature'],
        },
        sorted(result, key=lambda x: (-(x['water_temperature']), x['name']))
    ))

    headers = ['fjord', 'coast_length', 'depth', 'temperature']

    with open('suggestions.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=headers,
                                delimiter=',')
        if data:
            writer.writeheader()
        writer.writerows(data)


v = ["Norway", "Sweeden", "Chile", "New Zealand", "USA", "some"]
trip(300, v)
