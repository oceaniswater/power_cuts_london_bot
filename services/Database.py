import os
import psycopg2


# read database connection url from the enivron variable we just set (if you use heroku server).
# DATABASE_URL = os.environ.get('DATABASE_URL')
# or
DATABASE_URL = 'postgres://jhtgkxgfriekcn:f3dba6422af76e9f4ce9bc2cc44cdff74a1162129a37cecc97e1ca8d46083db5@ec2-54-204' \
               '-241-136.compute-1.amazonaws.com:5432/d2lsm2nlia511i'


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