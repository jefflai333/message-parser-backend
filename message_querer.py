import psycopg2

def query_aggregate_data_from_db():
    conn = psycopg2.connect(dbname="test", user="postgres", password="password", host="0.0.0.0", port="5433")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) from messages;")
    total_rows = cur.fetchone()
    print(total_rows, type(total_rows))
    conn.commit()
    cur.close()
    conn.close()
