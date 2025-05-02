from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from main import create_app  # or wherever your create_app is

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
