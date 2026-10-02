import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/sales.db")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)




def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        region TEXT NOT NULL,
        segment TEXT NOT NULL)
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_date TEXT NOT NULL,
        customer_id INTEGER NOT NULL,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        revenue REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id))
    ''')
    connection.commit()
    cursor.close()
    connection.close()



def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    customers = [
        (1, "ABC Technologies", "South", "Enterprise"),
        (2, "XYZ Retail", "North", "SMB"),
        (3, "Global Systems", "South", "Enterprise"),
        (4, "Modern Traders", "West", "Mid-Market"),
        (5, "Future Solutions", "East", "SMB"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, name, region, segment)
        VALUES (?, ?, ?, ?)
    """, customers)

    orders = [
        (1, 1, "2026-01-05", "Laptop", 5, 400000),
        (2, 1, "2026-01-15", "Monitor", 10, 150000),
        (3, 2, "2026-01-20", "Laptop", 2, 160000),
        (4, 3, "2026-02-05", "Server", 3, 600000),
        (5, 4, "2026-02-12", "Monitor", 20, 300000),
        (6, 5, "2026-03-01", "Laptop", 4, 320000),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, order_date, product, quantity, revenue)
        VALUES (?, ?, ?, ?, ?, ?)
    """, orders)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("Database created successfully.")