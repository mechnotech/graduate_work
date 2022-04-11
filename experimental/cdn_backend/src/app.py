from flasgger import Swagger
from flask import Flask
from views.links.links import links

app = Flask(__name__)
app.config.from_pyfile('settings.py', silent=True)

app.app_context().push()

swagger = Swagger(app, template_file='project_description/openapi.yaml')

app.register_blueprint(links, url_prefix='/api/v1/links')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', port=5000,
    )
