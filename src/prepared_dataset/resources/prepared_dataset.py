from flask_restful import Resource, reqparse
from util import combiner


class PreparedDatasetResource(Resource):
    def __init__(self):
        super(PreparedDatasetResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('format', type=str, required=True, location='json')
        self.parser.add_argument('patient_ids', type=str, required=True, location='json', action='append')
        self.parser.add_argument('fhir', type=dict, required=True, location='json')
        self.parser.add_argument('gemini', type=dict, required=True, location='json')

    def post(self):
        args = self.parser.parse_args()
        return combiner.get_omop_gemini_combined(args["format"], args["patient_ids"], args["fhir"], args["gemini"])
