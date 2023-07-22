from flask import Flask
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Da Vinci Coder Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


class DaVinciResponseSchema(Schema):
    message = fields.Str(default='Success')


class DaVinciRequestSchema(Schema):
    query = fields.String(required=True, description="Query to be sent to OpenAI")


#  Restful way of creating APIs through Flask Restful
class DaVinciAPI(MethodResource, Resource):
    @doc(description='GET Query Status', tags=['DaVinci'])
    @marshal_with(DaVinciResponseSchema)  # marshalling
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'Success'}

    @doc(description='POST Query.', tags=['DaVinci'])
    @use_kwargs(DaVinciRequestSchema, location=('json'))
    @marshal_with(DaVinciResponseSchema)  # marshalling
    def post(self, **kwargs):
        '''
        Post method represents a POST API method
        '''
        query = kwargs.get('query')
        return_from_openai = query

        return {'message': 'Return from OpenAI : ' + return_from_openai}


api.add_resource(DaVinciAPI, '/davinci')
docs.register(DaVinciAPI)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

