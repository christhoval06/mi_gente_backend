# from dataclasses import dataclass
# from sqlalchemy.dialects.postgresql import JSON

from marshmallow import fields
from marshmallow.validate import Length

from . import db, ma
from .mixin import AppModel

class Person(AppModel):
    __tablename__ = 'people'

    ndi = db.Column(db.String(15), unique=True)
    birthdate = db.Column(db.DateTime)
    names = db.Column(db.String(40))
    last_names = db.Column(db.String(40))

    contact = db.Column(db.String(20), nullable=True, default=None)
    address = db.Column(db.String(200), nullable=True, default=None)

    is_voted = db.Column(db.Boolean, default=False)
    voting_place = db.Column(db.String(200), nullable=True, default=None)
    voting_board = db.Column(db.String(10), nullable=True, default=None)
  
def get_person_schema(is_optional=False):
    
    class PersonSchema(ma.SQLAlchemySchema):
        class Meta:
            model = Person
            # fields = ('id','ndi','birthdate','names','last_names', 'contact', 'address', 'is_voted', 'voting_place', 'voting_board')
        
        id = fields.Int()

        ndi = fields.Str(required=not is_optional, validate=Length(min=1, max=15))
        birthdate = fields.DateTime(required=not is_optional)
        names = fields.Str(required=not is_optional, validate=Length(min=1, max=40))
        last_names = fields.Str(required=not is_optional, validate=Length(min=1, max=40))

        contact = fields.Str(validate=Length(min=1, max=20))
        address = fields.Str(validate=Length(min=1, max=200))

        is_voted = fields.Bool()
        voting_place = fields.Str(validate=Length(min=1, max=200))
        voting_board = fields.Str(validate=Length(min=1, max=20))

    return PersonSchema()

person_schema = get_person_schema()

# result_no_stop_words = db.Column(JSON)