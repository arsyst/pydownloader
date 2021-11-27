import sqlite3

connection = sqlite3.connect('norway_trip.db')
cursor = connection.cursor()

from_distance = int(input())
to_distance = int(input())

query = """
SELECT location, attraction, distance FROM Places
WHERE distance BETWEEN ? AND ?"""

result = cursor.execute(query, (from_distance, to_distance)).fetchall()

travel = list(map(
    lambda x: [x[0], x[1]],
    sorted(result, key=lambda x: (x[2], x[0]))
))
