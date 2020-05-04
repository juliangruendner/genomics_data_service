from flask_restful import Resource, reqparse
import util.gemini as Gemini


class VcfMergeResource(Resource):
    def __init__(self):
        super(VcfMergeResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('tool', type=str, required=True, location='json')
        self.parser.add_argument('filter_option', type=str, required=False, location='json')
        self.parser.add_argument('file_names', type=str, required=True, location='json', action='append')
        self.parser.add_argument('output_file_name', type=str, required=True, location='json')

    def post(self):
        args = self.parser.parse_args()
        filter_option = None
        if "filter_option" in args:
            filter_option = args['filter_option']
        return Gemini.merge(args['tool'], filter_option, args['file_names'], args['output_file_name'])
