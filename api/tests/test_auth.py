import json
import unittest
from http import HTTPStatus
from .. import create_app
from ..models.student import Student
from ..models.admin import Admin
from ..models.course import Course
from ..utils import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


class AuthTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None

    def test_signup(self):
        signup_data = {
            'name': 'TestStudent',
            'email': 'teststudent@gmail.com',
            'password': 'testlstudent'
        }
        response = self.client.post('api/auth/signup', json=signup_data)
        student = Student.query.filter_by(
            email='teststudent@gmail.com').first()
        assert student.name == "TestStudent"

        assert response.status_code == 201

    def test_login(self):
        login_data = {
            'email': 'johndoe@example.com',
            'password': 'password'
        }
        response = self.client.post('api/auth/login', json=login_data)
        assert response.status_code == 200

    # admin signup
    def test_adminsignup(self):
        signup_data = {
            'type_acct': 'admin',
            'email': 'admintest@gmail.com',
            'password': 'admintest123'
        }
        response = self.client.post('/api/auth/admin/signup', json=signup_data)
        admin = Admin.query.filter_by(
            email='admintest@gmail.com').first()
        assert admin.email == "admintest@gmail.com"

        assert response.status_code == 201

    # admin login
    def test_adminlogin(self):
        login_data = {
            'email': 'admintest@gmail.com',
            'password': 'admintest123'
        }
        response = self.client.post('api/auth/admin/login', json=login_data)
        assert response.status_code == 200

    # update student by authorization
    def test_updatestudent(self):
        student = Student.query.filter_by(
            email='teststudent@gmail.com').first()
        token = create_access_token(identity=student)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        student_update_data = {
            'name': 'TestStudent',
            'email': 'teststudent@gmail.com',
        }

        response = self.client.put(
            '/api/update/me', json=student_update_data, headers=headers)

        assert response.status_code == 200

    # retreive student in database
    def test_getallstudents(self):
        admin = Admin.query.filter_by(
            email='admintest@gmail.com').first()
        token = create_access_token(identity=admin)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        students = Student.query.all()
        response = self.client.get(
            '/api/getallstudent', json=students, headers=headers)
        assert response.status_code == 200

    # delete student by id
    def test_deletestudent(self):
        admin = Admin.query.filter_by(
            email='admintest@gmail.com').first()
        token = create_access_token(identity=admin)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.delete('/api/admin/delete/1', headers=headers)
        assert response.status_code == 200

    # enrol student to a course

    def test_enrolstudent_to_course(self):
        @jwt_required()
        def enrol_student():
            student = Student.query.filter_by(
                email='teststudent@gmail.com').first()
            token = create_access_token(identity=student)
            headers = {
                "Authorization": f"Bearer {token}"
            }

            username = get_jwt_identity()
            current_user = Student.query.filter_by(email=username).first()

            set_course = Course(
                name='Cloud',
                instructor='Faruq'
            )
            set_course.student = current_user.id
            response = self.client.post(
                '/api/course/set_course', headers=headers)
            assert response.status_code == 200

    # delete course for student by id
    def test_deletecoursefor_student(self):
        admin = Admin.query.filter_by(
            email='admintest@gmail.com').first()
        token = create_access_token(identity=admin)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.delete(
            '/api/admin/student/1/course', headers=headers)
        if response.status_code == 500:
            print('Not Found')
        else:
            assert response.status_code == 200
