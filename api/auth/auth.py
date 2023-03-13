from flask_restx import Resource, Namespace, fields
from flask import request, make_response
from ..models.student import Student
from http import HTTPStatus
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies, get_jwt


auth_namespace = Namespace(
    'auth', description="Authentication for student management api")

signup_model = auth_namespace.model('SignUp', {
    'id': fields.Integer(),
    'name': fields.String(required=True, description='Student name'),
    'email': fields.String(required=True, description='Student email address'),
    'password': fields.String(required=True, description='Student password')
})
login_model = auth_namespace.model('Login', {
    'email': fields.String(required=True, description='Student email address'),
    'password': fields.String(required=True, description='Student password')
})

# Path for registering new Student


@auth_namespace.route('/signup')
class SignUpAuth(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        '''
            SignUp authentication for new users
        '''
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = generate_password_hash(data['password'])

        new_user = Student(name=name, email=email, password=password)
        new_user.save()

        return new_user, HTTPStatus.CREATED

# Path for verifying Student


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        '''
            Generate JWT Tokens for Students
        '''
        data = request.get_json()
        email = data['email']
        user = Student.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            response = {
                'create_access_token': access_token,
                'create_refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED

# Path for getting refresh tokens


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        '''
            Generate Refresh token
        '''
        email = get_jwt_identity()
        refresh_token = create_refresh_token(identity=email)
        access_token = create_access_token(identity=email)

        response = {
            'refresh_token': refresh_token,
            'access_token': access_token
        }
        return response, HTTPStatus.OK

# Path for getting student username


@auth_namespace.route('/getme')
class GetUser(Resource):
    @jwt_required()
    def get(self):
        '''
            Get user name and email
        '''
        current_user = get_jwt_identity()
        student = Student.query.filter_by(email=current_user).first()
        name = student.name
        response = {
            'email': current_user,
            'username': name
        }

        return response, HTTPStatus.OK

# Path to logout user


@auth_namespace.route('/logout')
class LogOut(Resource):
    @jwt_required()
    def post(self):
        '''
            Logout User
        '''
        response = make_response({'message': 'Logout successful'})
        unset_jwt_cookies(response)
        return response
