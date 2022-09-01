import os
import tornado.template

from tornado.options import define
from rewardsservice.error_handling.error_handling import ErrorHandler

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

define("port", default=7050, help="run on the given port", type=int)


# added default handler class and args for error handling. 
settings = {
    'debug': True,
    'static_path': STATIC_ROOT,
    'template_loader': tornado.template.Loader(TEMPLATE_ROOT),
    'default_handler_class': ErrorHandler,
    'default_handler_args': dict(status_code=404)
}
