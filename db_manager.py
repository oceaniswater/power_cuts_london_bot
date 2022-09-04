from services.Database import Database


# insert user
async def insert_user(telegram_id):
    connection = Database.create_connection()
    cur = connection.cursor()
    await cur.execute(f'INSERT INTO users(telegram_id, postcode) VALUES (%s, %s)',
                (telegram_id, None))

    connection.commit()
    cur.close()
    connection.close()

# check user exist
async def check_user(telegram_id):
    connection = Database.create_connection()
    cur = connection.cursor()
    try:
        await cur.execute(f'SELECT telegram_id FROM users WHERE telegram_id = {telegram_id}')
        records = cur.fetchone()
        cur.close()
        connection.close()
        print(f"запись есть в бд{records[0][0]}")
        return records[0][0]
    except:
        cur.close()
        connection.close()
        print(f"записи нет в бд")
        return 0