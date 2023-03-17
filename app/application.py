from flask import Flask

from .containers import Container
from . import views

def create_app():
    container = Container()
    app = Flask(__name__)
    app.container = container
    app.add_url_rule('/', 'index', views.index)
    app.add_url_rule('/process/<proc_id>', 'process', views.process)
    app.add_url_rule('/process/new', 'new_process', views.new_process)
    app.add_url_rule('/process/create', 'create_process', views.create_process, methods=['POST'])
    app.add_url_rule('/process/upload/<proc_id>', 'upload', views.upload, methods=['POST'])
    app.add_url_rule('/process/validate/<proc_id>', 'validate', views.validate, methods=['GET'])
    return app

