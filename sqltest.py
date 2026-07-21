import sqlite3
import main


main.maketable()
main.pre_tsuika()


with sqlite3.connect('lib_sys.db') as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM name")
    print(cur.fetchone())

