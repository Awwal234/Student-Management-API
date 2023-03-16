from flask import Flask
from flask_restx import Api
from .auth.auth import auth_namespace
from .course.course import course_namespace
from .getstudent.views import student_namespace
from .admin.views import admin_namespace
from .updates.UpdateStudent import update_namespace
from .admin_auth.views import admin_auth_namespace
from .grading.grading import grading_namespace
from flask_jwt_extended import JWTManager
from datetime import timedelta
from .utils import db
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest, InternalServerError


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd731e034c39e798bbf0f1a6c'
    app.config['JWT_SECRET_KEY'] = 'c731e054c39e798bbf0f1a5c'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    migrate = Migrate(app, db)
    api = Api(app, title='Student Management API',
              description='student management api designed by Dolapo, a student of ALTSCHOOL AFRICA')
    api.add_namespace(auth_namespace, path='/api/auth')
    api.add_namespace(course_namespace, path='/api/course')
    api.add_namespace(student_namespace, path='/api')
    api.add_namespace(admin_namespace, path='/api/admin')
    api.add_namespace(update_namespace, path='/api/update')
    api.add_namespace(admin_auth_namespace, path='/api/auth/admin')
    api.add_namespace(grading_namespace, path='/api/auth/admin/grading')

    @api.errorhandler(BadRequest)
    def handle_bad_request_error(error):
        return {'message': 'Bad Request Error'}, 400

    @api.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        return {'message': 'DataBase Error'}, 500

    @api.errorhandler(NotFound)
    def handle_bad_request_error(error):
        return {'message': 'Not Found'}, 400

    @api.errorhandler(MethodNotAllowed)
    def handle_internal_server_error(error):
        return {'message': 'Method Not Allowed'}, 400
    
    return app
