import json
from flask import session,redirect
from werkzeug.wrappers import Request
from datetime import datetime
import insert

import psycopg2


class SimpleMiddleware(object):
    def __init__(self,app):
        self.app=app
        self.client = psycopg2.connect(database="Test", user="postgres", password="admin@123", host="localhost", port="5432")
        self.client.autocommit = True
        self.cursor = self.client.cursor()

    def __call__(self,environ,startresponse):
       try:
           request = Request(environ)
           name=request.environ["HTTP_COOKIE"][8:]
           plc=insert.GetUsername(name)
           print(request,"helloworld")

           # hello=json.dumps(environ)
           self.cursor.execute(f"INSERT INTO public.logs(text)VALUES ('called');")
           print(request.environ,"name",plc)
           return self.app(environ, startresponse)
       except Exception as e:
           print(e,"hello")


