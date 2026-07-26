import sqlite3

conn = sqlite3.connect('/app/traces.db'); 

rows = conn.execute(
    'SELECT  s.input_tokens FROM spans s where s.name="llm"'
    ).fetchall()

for row in rows:
    print(row)