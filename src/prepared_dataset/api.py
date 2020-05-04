from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.prepared_dataset import PreparedDatasetResource

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(PreparedDatasetResource, '/prepared_dataset', endpoint='prepared_dataset')

if __name__ == '__main__':
    # set false in production mode
    app.run(debug=True, host='0.0.0.0', port=5000)
