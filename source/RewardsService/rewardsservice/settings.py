import os
import tornado.template
from tornado.options import define

# Define a lambda function to construct file paths
path = lambda root, *a: os.path.join(root, *a)

# Get the absolute path of the current directory
ROOT = os.path.dirname(os.path.abspath(__file__))

# Define the paths for static files and templates
STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

# Define a Tornado option for the port
define("port", default=7050, help="Run on the given port", type=int)

# Configuration settings for the Tornado application
settings = {
    'debug': True,  # Enable debug mode for better error messages
    'static_path': STATIC_ROOT,  # Path to static files
    'template_loader': tornado.template.Loader(TEMPLATE_ROOT)  # Template loader for rendering HTML templates
}

