from datetime import datetime
from flask.cli import FlaskGroup

from app import app
from app.models import db, Person


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Person(ndi="5-706-1803", names="Christhoval", last_names="Barba Rivas", birthdate=datetime.strptime("01/06/1989", "%m/%d/%Y")))
    db.session.commit()


if __name__ == "__main__":
    cli()