import os
import tornado.template

from tornado.options import define

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

define("port", default=7050, help="run on the given port", type=int)

MONGO_HOST = os.environ.get("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "Rewards")

settings = {
    'debug': True,
    'static_path': STATIC_ROOT,
    'template_loader': tornado.template.Loader(TEMPLATE_ROOT)
}
