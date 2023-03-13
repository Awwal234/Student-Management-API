from flask_restx import Resource, Namespace, fields
from flask import request, make_response
from ..models.student import Student
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db
from http import HTTPStatus

update_namespace = Namespace(
    'updates', description="Update Info for student management api")

# The Only thing to Update for user is email and name
signup_model_schema = update_namespace.model('Schema', {
    'id': fields.Integer(),
    'name': fields.String(required=True, description='Student name'),
    'email': fields.String(required=True, description='Student email address'),
    'password': fields.String(required=True, description='Student password')
})

update_model = update_namespace.model('Update', {
    'email': fields.String(required=True, description='Student email address'),
    'name': fields.String(required=True, description='Student name')
})

# route to update student email and name


@update_namespace.route('/me')
class UpdateStudentInfo(Resource):
    @update_namespace.expect(update_model)
    @update_namespace.marshal_with(signup_model_schema)
    @jwt_required()
    def put(self):
        '''
            Update Specific Student Info Through Authorization
        '''
        data = update_namespace.payload
        # data_data = request.get_json()
        email = get_jwt_identity()
        search_by = Student.query.filter_by(email=email).first()

        if search_by:
            search_by.email = data['email']
            search_by.name = data['name']

            db.session.commit()

            return search_by, HTTPStatus.OK
