"""
Base handler to set header defaults for all other request handlers
and to set CLIENT const
"""
import tornado.web

from pymongo import MongoClient

class BaseHandler(tornado.web.RequestHandler):
    CLIENT = MongoClient("mongodb", 27017)

    def set_default_headers(self):
        """
        Set the default headers to application/json for Accept and Content-Type
        """
        self.set_header('Accept', 'application/json')
        self.set_header('Content-Type', 'application/json')
