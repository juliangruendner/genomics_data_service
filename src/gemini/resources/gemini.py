from flask_restful import Resource, reqparse, abort
from flask import make_response
import util.gemini as Gemini
import traceback

Gemini.make_directories()


class GeminiDbsResource(Resource):
    def __init__(self):
        super(GeminiDbsResource, self).__init__()

    def get(self):
        return Gemini.get_gemini_dbs()


class GeminiDbResource(Resource):
    def __init__(self):
        super(GeminiDbResource, self).__init__()

    def get(self, db_name):
        return Gemini.send_gemini_db(db_name)


class GeminiQueryResource(Resource):
    def __init__(self):
        super(GeminiQueryResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('db_name', type=str, required=True, location='json')
        self.parser.add_argument('query', type=str, required=True, location='json')
        self.parser.add_argument('skip', type=int, required=False, location='json')
        self.parser.add_argument('limit', type=int, required=False, location='json')

    def post(self):
        args = self.parser.parse_args()
        try:
            ret = Gemini.query(args["db_name"], args["query"], args["skip"], args["limit"])
        except Exception as e:
            traceback.print_exc()
            abort(400, message=e.output.decode("utf-8"))
        resp = make_response(ret, 200)
        return resp


class GeminiQueryVariantsResource(Resource):
    def __init__(self):
        super(GeminiQueryVariantsResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('db_name', type=str, required=True, location='json')
        self.parser.add_argument('skip', type=int, required=False, location='json')
        self.parser.add_argument('limit', type=int, required=False, location='json')

    def post(self):
        args = self.parser.parse_args()
        ret = Gemini.query_variants(args["db_name"], args["skip"], args["limit"])
        resp = make_response(ret, 200)
        return resp
