
from sqlalchemy import func, case
from sqlalchemy.sql import label


from app.auth import api_key_required
from app.models import db
from app.models.person import Person

def init(app):

    @app.route('/api/voting_place', methods=['GET'])
    @api_key_required
    def get_voting_places():
        result = Person.query.filter(Person.is_voted==True).with_entities(Person.voting_place).distinct().all()
        result = [place for (place,) in result]
        return result, 200


    @app.route('/api/voting_place/stats', methods=['GET'])
    @api_key_required
    def get_voting_place_stats():

        result = db.session.query(
            label('voting_place', Person.voting_place),
            func.sum(case((Person.is_voted == True, 1), else_=0)).label('votes'),
            func.sum(case((Person.is_voted == False, 1), else_=0)).label('no_votes')
            ).group_by(Person.voting_place).order_by(Person.voting_place).all()
        
        print(result)
        
        result = [{"place": place, "votes": votes, 'no_votes':no_votes} for (place, votes, no_votes) in result]
        return result, 200


    @app.route('/api/voting_place/<string:votes>/votes', methods=['GET'])
    @api_key_required
    def get_votes_by_voting_place(votes):

        filters = []
        
        if votes in ['si', 'no']:
            filters.append(Person.is_voted==(True if votes=='si' else False))

        result = db.session.query(
            label('voting_place', Person.voting_place),
            func.count(Person.voting_place)
            ).filter(*filters).group_by(Person.voting_place).order_by(Person.voting_place).all()
        
        result = [{"place": place, "count": count} for (place, count) in result]
        return result, 200
