from flask_restful import Resource, reqparse, abort
import util.gemini as Gemini
import werkzeug


class VcfLoadResource(Resource):
    def __init__(self):
        super(VcfLoadResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('files', type=werkzeug.datastructures.FileStorage, required=True, location='files', action='append')

    def post(self):
        args = self.parser.parse_args()
        files = args['files']
        for f in files:
            if not f.filename.endswith(".vcf"):
                m = f.filename + " does not end with .vcf and is therefore not recognized as a valid vcf file!"
                abort(400, message=m)
        return Gemini.load_vcf_files(files)


class VcfGeminiLoadResource(Resource):
    def __init__(self):
        super(VcfGeminiLoadResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('vcf_file', type=str, required=True, location='args')
        self.parser.add_argument('db_name', type=str, required=True, location='args')

    def post(self):
        args = self.parser.parse_args()
        return Gemini.execute_pipeline(args["vcf_file"], args["db_name"])
