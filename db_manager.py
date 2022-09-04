from services.Database import Database


# insert user
def insert_user(telegram_id):
    connection = Database.create_connection()
    cur = connection.cursor()
    cur.execute(f'INSERT INTO users(telegram_id, postcode) VALUES (%s, %s)',
                (telegram_id, None))
    connection.commit()
    cur.close()
    connection.close()