from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import os
import boto3
import mysql.connector

DATABASE_REGION = 'ap-northeast-1'
DATABASE_CERT = 'cert/ap-northeast-1-bundle.pem'
DATABASE_HOST = os.environ['DB_HOST']
DATABASE_PORT = os.environ['DB_PORT']
DATABASE_USER = os.environ['DB_USER']
DATABASE_NAME = os.environ['DB_NAME']
PORT = 8080

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

rds = boto3.client('rds', region_name=DATABASE_REGION)

try:
    token = rds.generate_db_auth_token(
        DBHostname=DATABASE_HOST,
        Port=DATABASE_PORT,
        DBUsername=DATABASE_USER,
        Region=DATABASE_REGION
    )
    # print(token)
    mydb =  mysql.connector.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        passwd=token,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
        ssl_ca=DATABASE_CERT
    )
except Exception as e:
    print('Database connection failed due to {}'.format(e))          

def all_books(request):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT name, title, year FROM authors, books WHERE authors.authorId = books.authorId ORDER BY year')
    title = 'Books'
    message = '<html><head><title>' + title + '</title></head><body>'
    message += '<h1>' + title + '</h1>'
    message += '<ul>'
    for (name, title, year) in mycursor:
        message += '<li>' + name + ' - ' + title + ' (' + str(year) + ')</li>'
    message += '</ul>'
    message += '</body></html>'
    return Response(message)

if __name__ == '__main__':

    with Configurator() as config:
        config.add_route('all_books', '/')
        config.add_view(all_books, route_name='all_books')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()

