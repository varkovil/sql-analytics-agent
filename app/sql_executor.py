from app.database import get_connection


def execute_sql(sql):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        return columns, results, None

    except Exception as e:
        return [], [], str(e)

    finally:
        cursor.close()
        connection.close()