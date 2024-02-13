
from flask import jsonify, request

from app.auth import api_key_required
from app.models.person import Person, person_schema, get_person_schema

def init(app):

    @app.route('/api/people', methods=['GET'])
    @api_key_required
    def get_people():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per-page", 100, type=int)

        query = Person.query

        voting_board = request.args.get("voting_board", None, type=str)
        voting_place = request.args.get("voting_place", None, type=str)
        ndi = request.args.get("ndi", None, type=str)

        if voting_board:
            query = query.filter(Person.voting_board == voting_board)
        if voting_place:
            query = query.filter(Person.voting_place == voting_place)
        if ndi:
            query = query.filter(Person.ndi == ndi)

        people = query.paginate(page=page, per_page=per_page)

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
