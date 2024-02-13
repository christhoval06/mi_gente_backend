
from sqlalchemy import func
from sqlalchemy.sql import label

from app.auth import api_key_required
from app.models import db
from app.models.person import Person, person_schema, get_person_schema

def init(app):

    @app.route('/api/voting_place', methods=['GET'])
    def get_voting_places():
        result = Person.query.filter(Person.is_voted==True).with_entities(Person.voting_place).distinct().all()
        result = [place for (place,) in result]
        return result, 200


    @app.route('/api/voting_place/stats', methods=['GET'])
    @api_key_required
    def get_voting_place_stats():
        result = db.session.query(label('voting_place', Person.voting_place),  func.count(Person.voting_place)).group_by(Person.voting_place).all()
        result = [{"place": place, "count": count} for (place, count) in result]
        return result, 200


    @app.route('/api/voting_place/votes', methods=['GET'])
    @api_key_required
    def get_votes_by_voting_place():
        result = db.session.query(label('voting_place', Person.voting_place),  func.count(Person.voting_place)).filter(Person.is_voted==True).group_by(Person.voting_place).all()
        result = [{"place": place, "count": count} for (place, count) in result]
        return result, 200
