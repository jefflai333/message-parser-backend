import psycopg2

def query_aggregate_data_from_db():
    conn = psycopg2.connect(dbname="test", user="postgres", password="password", host="localhost", port="5433")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) from messages;")
    total_rows = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return total_rows
