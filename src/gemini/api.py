from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.gemini import GeminiDbsResource, GeminiDbResource, GeminiQueryResource, GeminiQueryVariantsResource
from resources.vcf_load import VcfGeminiLoadResource, VcfLoadResource
from resources.vcfs import VcfsResource, VcfResource
from resources.vcf_merge import VcfMergeResource


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(GeminiDbsResource, '/gemini/dbs', endpoint='gemini_dbs')
api.add_resource(GeminiDbResource, '/gemini/dbs/<string:db_name>', endpoint='gemini_db')
api.add_resource(GeminiQueryResource, '/gemini/query', endpoint='gemini_query')
api.add_resource(GeminiQueryVariantsResource, '/gemini/query/variants', endpoint='gemini_query_variants')
api.add_resource(VcfGeminiLoadResource, '/gemini/import_vcf', endpoint='import_vcf')
api.add_resource(VcfLoadResource, '/gemini/upload_vcf', endpoint='upload_vcf')
api.add_resource(VcfsResource, '/gemini/vcfs', endpoint='vcfs')
api.add_resource(VcfResource, '/gemini/vcfs/<string:vcf_name>', endpoint='vcf')
api.add_resource(VcfMergeResource, '/gemini/vcfs/merge', endpoint='vcf_merge')


if __name__ == '__main__':
    # set false in production mode
    app.run(debug=False, host='0.0.0.0', port=5000)
