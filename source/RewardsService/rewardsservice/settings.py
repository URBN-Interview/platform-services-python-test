import os
from pymongo import MongoClient
import tornado.template

from tornado.options import define

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

define("port", default=7050, help="run on the given port", type=int)

db = MongoClient("mongodb", 27017)["Rewards"]

settings = {
    'debug': True,
    'static_path': STATIC_ROOT,
    'template_loader': tornado.template.Loader(TEMPLATE_ROOT),
    'db': db
}
