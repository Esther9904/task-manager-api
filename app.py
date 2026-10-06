from flask import Flask
from extensions import db
from routes import bp


def create_app(database_uri="sqlite:///tasks.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)
    app.register_blueprint(bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)