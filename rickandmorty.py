import sqlite3
import requests


url = 'https://rickandmortyapi.com/api/character'
characters = []

while url:
    response = requests.get(url)
    data = response.json()
    characters.extend(data['results'])
    url = data['info']['next']  


conn = sqlite3.connect('rickmorty.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    gender TEXT,
    origin TEXT
)
''')


for char in characters:
    cursor.execute('''
    INSERT OR REPLACE INTO characters (id, name, status, species, gender, origin)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        char['id'],
        char['name'],
        char['status'],
        char['species'],
        char['gender'],
        char['origin']['name']
    ))

conn.commit()


print("\nเพศของตัวละคร:")
cursor.execute('''
SELECT gender, COUNT(*) as count
FROM characters
GROUP BY gender
''')
for row in cursor.fetchall():
    print(row)


print("\nสถานะของตัวละคร:")
cursor.execute('''
SELECT status, COUNT(*) AS total
FROM characters
GROUP BY status;
''')
for row in cursor.fetchall():
    print(row)


print("\nต้นกำเนิดยอดนิยม:")
cursor.execute('''
SELECT origin, COUNT(*) as count
FROM characters
GROUP BY origin
ORDER BY count DESC
LIMIT 5
''')
for row in cursor.fetchall():
    print(row)

print("\nจำนวนตัวละครต่อสายพันธุ์:")
cursor.execute('''
SELECT species, COUNT(*) AS total
FROM characters
GROUP BY species
ORDER BY total DESC;
''')
for row in cursor.fetchall():
    print(row)

conn.close()
