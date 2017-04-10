from contextlib import closing
import sqlite3

session_dbname = 'vr_sessions.sqlite3'

with closing(sqlite3.connect(session_dbname)) as conn:
    c = conn.cursor()

    # Create Table
    try:
        c.execute("""DROP TABLE sessions""")
    except sqlite3.OperationalError:  # If table didn't exist
        pass

    c.execute("""CREATE TABLE sessions
                (experiment text, rat text)
                """)
    conn.commit()


