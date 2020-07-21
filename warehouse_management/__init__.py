import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    # create and configure the app
    
    app = Flask(__name__, instance_relative_config=True)
    
    bootstrap = Bootstrap(app)


    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'warehouse_management.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template(
            "home.html"
        )
    from . import location
    app.register_blueprint(location.bp)

    from . import product
    app.register_blueprint(product.bp)
    
    from . import product_movement
    app.register_blueprint(product_movement.bp)
    



    from . import db
    db.init_app(app)

    return app