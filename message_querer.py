import psycopg2


class MessageQuerer:
    def __init__(self) -> None:
        pass

    def query_aggregate_data_from_db():
        conn = psycopg2.connect(dbname="test", user="postgres",
                                password="password", host="localhost", port="5433")
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*), COUNT(CASE WHEN title=sender then 1 ELSE NULL END), COUNT(CASE WHEN title!=sender then 1 ELSE NULL END) from messages;")
        # print(cur.fetchone())
        # if cur.fetchone() is None:
        #     print("cur.fetchone is None")
        #     total_rows = (0, 0, 0)
        # else:
        #     print("cur.fetchone is NOT None")
        total_rows = cur.fetchone()
        cur.execute("SELECT title from messages GROUP BY title;")
        # if cur.fetchone() is None:
        #     total_rows = total_rows + ("",)
        total_rows = total_rows + cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return total_rows
