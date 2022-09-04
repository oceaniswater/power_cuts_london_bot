import os
import psycopg2


# read database connection url from the enivron variable we just set (if you use heroku server).
DATABASE_URL = os.environ.get('DATABASE_URL')


class Database:
    @staticmethod
    def create_connection():
        connection = None
        try:
            # create a new database connection by calling the connect() function
            connection = psycopg2.connect(DATABASE_URL)
            print('connection successful')
        except Exception as error:
            print('Cause: {}'.format(error))

        return connection