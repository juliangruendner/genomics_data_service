from flask_restful import Resource
import util.gemini as Gemini


class VcfsResource(Resource):
    def __init__(self):
        super(VcfsResource, self).__init__()

    def get(self):
        return Gemini.get_vcf_files()


class VcfResource(Resource):
    def __init__(self):
        super(VcfResource, self).__init__()

    def get(self, vcf_name):
        return Gemini.send_vcf(vcf_name)
