import psycopg2


def query_aggregate_data_from_db():
    try:
        conn = psycopg2.connect(dbname="test", user="postgres",
                            password="password", host="localhost", port="5433")
    except Exception as err:
        print("error msg:", err)
        conn = None
    if conn != None:
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*), COUNT(CASE WHEN title=sender then 1 ELSE NULL END), COUNT(CASE WHEN title!=sender then 1 ELSE NULL END) from messages;")
        total_rows = cur.fetchone()
        cur.execute("SELECT title from messages GROUP BY title;")
        total_rows = total_rows + cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return total_rows
    return None
