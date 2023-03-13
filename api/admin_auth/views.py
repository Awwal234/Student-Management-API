from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus

admin_auth_namespace = Namespace(
    'admin_auth', description="Authentication for admin")

admin_model = admin_auth_namespace.model('Admin', {
    'email': fields.String(required=True, description='Admin email address'),
    'password': fields.String(required=True, description='Admin password'),
    'type_acct': fields.String(required=True, description='Admin account type', default='admin')
})

admin_login_model = admin_auth_namespace.model('Login_Admin', {
    'email': fields.String(required=True, description='Admin email address'),
    'password': fields.String(required=True, description='Admin password'),
})


@admin_auth_namespace.route('/signup')
class AdminSignUp(Resource):
    @admin_auth_namespace.expect(admin_model)
    @admin_auth_namespace.marshal_with(admin_model)
    def post(self):
        '''
            Authenticate Signup for admin
        '''
        data = request.get_json()
        email = data['email']
        type_acct = data['type_acct']
        password = generate_password_hash(data['password'])

        new_admin = Admin(email=email, password=password, type_acct=type_acct)
        new_admin.save()

        return new_admin, HTTPStatus.CREATED


@admin_auth_namespace.route('/login')
class AdminLogin(Resource):
    @admin_auth_namespace.expect(admin_login_model)
    def post(self):
        '''
            Authenticate Login for admin
        '''
        data = admin_auth_namespace.payload
        email = data['email']
        user = Admin.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            response = {
                'create_access_token': access_token,
                'create_refresh_token': refresh_token,
                'type': 'admin'
            }

            return response, HTTPStatus.CREATED
