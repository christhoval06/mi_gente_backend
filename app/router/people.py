
import functools
from app.utils.tuples import tuple_reducer
from flask import jsonify, request
from sqlalchemy import extract, func, case
from sqlalchemy.sql import label

from app.auth import api_key_required
from app.models import db
from app.models.person import Person, person_schema, get_person_schema

def init(app):

    @app.route('/api/people', methods=['GET'])
    @api_key_required
    def get_people():
        query = Person.query
        filters = []

        if voting_board := request.args.get("voting_board", None, type=str):
            filters.append(Person.voting_board == voting_board)
        if voting_place := request.args.get("voting_place", None, type=str):
            filters.append(Person.voting_place == voting_place)
        if ndi := request.args.get("ndi", None, type=str):
            filters.append(Person.ndi == ndi)

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 100, type=int)

        query = query.filter(*filter)


        people = query.paginate(page=page, per_page=per_page).order_by(Person.updated_at.desc())

        results = {
            "results": person_schema.dump(people.items, many=True),
            "pagination": {
                "count": people.total,
                "page": page,
                "per_page": per_page,
                "pages": people.pages,
            },
        }
        return jsonify(results), 200

    @app.route('/api/people/<int:id>', methods=['GET'])
    @api_key_required
    def get_person(id):
        person = Person.query.get(id)
        if person is None:
            return jsonify(error="person not found", errno=1), 403
        
        result = person_schema.dump(person)

        return result, 200

    @app.route('/api/people', methods=['POST'])
    @api_key_required
    def set_person():
        result = person_schema.load(request.json)
        person = Person(**result)
        person.save()
        
        result = person_schema.dump(person)
        return result, 200

    @app.route('/api/people/<int:id>', methods=['PUT'])
    @api_key_required
    def put_person(id):
        person = Person.query.get(id)
        if person is None:
            return jsonify(error="person not found", errno=1), 403
        

        result = person_schema.load(request.json)

        person = person.update(**result)
        
        result = person_schema.dump(person)
        return result, 200


    @app.route('/api/people/<int:id>', methods=['PATCH'])
    @api_key_required
    def patch_person(id):
        person = Person.query.get(id)
        if person is None:
            return jsonify(error="person not found", errno=1), 403
        
        schema = get_person_schema(True)
        result = schema.load(request.json)
        person = person.update(**result)
        
        result = person_schema.dump(person)
        return result, 200
    
    @app.route('/api/people/provinces/votes/<string:votes>/count', methods=['GET'])
    @api_key_required
    def people_provinces_votes_count(votes):

        provinces = [
            ('1', 'Bocas del Toro'),
            ('2', 'Coclé'),
            ('3', 'Colón'),
            ('4', 'Chiriquí'),
            ('5', 'Darién'),
            ('6', 'Herrera'),
            ('7', 'Los Santos'),
            ('8', 'Panamá'),
            ('9', 'Veraguas'),
            ('10', 'Guna Yala'),
            ('11', 'Emberá Wounaan'),
            ('12', 'Ngäbe-Buglé'),
            ('13', 'Panamá Oeste')
        ]
        
        filters = []
        
        if votes in ['si', 'no']:
            filters.append(Person.is_voted==(True if votes=='si' else False))

        provinces_case = [(func.split_part(Person.ndi, '-', 1) == prefix, province) for (prefix, province) in provinces]

        case_statement = case(*provinces_case,else_='Panamá')

        result = db.session.query(
            label('province', case_statement),
                func.count(case_statement).label('province_count'),
        ).group_by('province').filter(*filters).order_by('province').all()


        # result = db.session.query(
        #     label('province',  func.split_part(Person.ndi, '-', 1)),
        #     func.count(func.split_part(Person.ndi, '-', 1))
        #     ).group_by('province').filter(*filters).order_by('province').all()

        result = [{"province": province, "count": count} for (province, count) in result]

        return result, 200
    
    @app.route('/api/people/age/votes/<string:votes>/count', methods=['GET'])
    @api_key_required
    def people_age_votes_count(votes):

        # https://code.likeagirl.io/sql-alchemy-python-functions-part2-case-707eb7e95891

        filters = []

        if votes in ['si', 'no']:
            filters.append(Person.is_voted==(True if votes=='si' else False))

        age_groups = [(70, 'F'), (60, 'E'), (50, 'D'), (40, 'C'), (30, 'B'), (18, 'A')]
        age_cases = [(extract('year', func.age(Person.birthdate)) >= value, group) for (value, group) in age_groups]
        case_statement = case(*age_cases, else_='Z')
        
        
        result = db.session.query(
            label('age_group', case_statement),
                func.count(case_statement).label('age_group_count'),
        ).group_by('age_group').filter(*filters).all()

        # result = [{f'{age_group}': count} for (age_group, count) in result]
        result = functools.reduce(tuple_reducer , result, {})
    
        return result, 200

        # ranges = [[0, 17, 'Z'], [18, 29, 'A'], [30, 39, 'B'], [40, 49, 'C'], [50, 59, 'D'], [60, 69, 'E'], [70, 2000, 'F']]

        # filters = []
        
        # if votes in ['si', 'no']:
        #     filters.append(Person.is_voted==(True if votes=='si' else False))


        # result = db.session.query(
        #     label('person_age', extract('year', func.age(Person.birthdate))),  
        #     func.count(extract('year', func.age(Person.birthdate)))
        #     ).group_by('person_age').filter(*filters).all()

        # def reducer(acc, el):
        #     (age, count)= el

        #     range = [group for [start, end, group] in ranges if age >= start and age <= end]
        #     range = range[0]
        #     acc[range] = acc.get(range, 0) + count 

        #     return acc
            
        # result = dict(functools.reduce(reducer, result, {}))
    
        # return result, 200
    

    @app.route('/api/people/votes/<string:votes>/count', methods=['GET'])
    @api_key_required
    def people_votes_count(votes):

        filters = []

        if votes in ['si', 'no']:
            filters.append(Person.is_voted==(True if votes=='si' else False))



        case_statement = case(
                (Person.is_voted == True, 'Si'),
                else_='No')
        
        result = db.session.query(
            label('voted_group', case_statement),
                func.count(case_statement).label('voted_group_count'),
        ).group_by('voted_group').filter(*filters).all()

        result = functools.reduce(tuple_reducer , result, {})

        return result, 200