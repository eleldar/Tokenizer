import os
from flask import Flask
from flask_restx import Resource, Api, fields
from flask_cors import CORS, cross_origin
from argparse import ArgumentParser
from api.tokenization import tokenize


app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
api = Api(
    app, 
    version='1.0',
    title='Tokenizer',
    doc="/api",
)

CORS(app)
namespace = api.namespace('tokenisation', 
#    description='Tokenisation'
)

tokenised_sequence = api.model('TokenizedSequence', {
    'sequence': fields.String
})


#extanded_words = api.model('ExtandedWords', {
#    'words': fields.String
#})


input_info = api.model('ResultInfo', {
    'text': fields.String
})

upload_parser = api.parser()

@namespace.route('/tokenize')
class DetectApi(Resource):
    @namespace.doc('ProcessedText')
    @namespace.expect(input_info)
    @namespace.marshal_with(tokenised_sequence, code=200)
    @namespace.response(404, 'No results')
    def post(self):
        data = api.payload
        text = data['text']
        result = tokenize(text)
        if result:
            return {'sequence': result}, 200 
        else:
            return {'sequence': result}, 404 


#@namespace.route('/extand')
#class DetectApi(Resource):
#    @namespace.doc('ProcessedVocab')
#    @namespace.expect(input_info)
#    @namespace.marshal_with(extanded_words, code=200)
#    @namespace.response(404, 'No results')
#    def post(self):
#        data = api.payload
#        text = data['text']
#        result = 'function into process development :-'
#        if result:
#            return {'words': result}, 200 
#        else:
#            return {'words': result}, 404 


if __name__ == '__main__':
    default_host = '0.0.0.0'
    default_port = '4000'

    parser = ArgumentParser()

    parser.add_argument(
        "-ht", "--host", dest="host", default=default_host,
        help=f'Enter connect host; default="{default_host}"'
    )
    parser.add_argument(
        "-p", "--port", dest="port", default=default_port,
        help=f'Enter connect port; default="{default_port}"'
    )
    args = parser.parse_args()

    app.run(
        host = args.host,
        port = args.port,
        debug=True
    )





