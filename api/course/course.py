from flask_restx import Resource, Namespace, fields
from flask import request
from ..models.course import Course
from ..models.student import Student
from ..models.grades import Grade
from ..models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

course_namespace = Namespace(
    'course', description='CRUD for courses with paths')

course_get_model = course_namespace.model('CoursePlace', {
    'id': fields.Integer(),
    'name': fields.String(required=True, description='Course name', enum=['FrontEnd', 'BackEnd', 'Cloud']),
    'instructor': fields.String(required=True, description='Course instructor')
})


@course_namespace.route('/getall_course')
class GetAllCourses(Resource):
    @jwt_required()
    def get(self):
        '''
         Get all courses in database with Authorization
        '''
        course = {
            'FrontEnd': 'FrontEnd Engineering',
            'BackEnd': 'BackEnd Engineering',
            'Cloud': 'Cloud Engineering'
        }
        return course, HTTPStatus.OK

# route for getting course by a specific student using their name


@course_namespace.route('/getme/get_course')
class GetCourseBySpecificUser(Resource):
    @course_namespace.marshal_with(course_get_model)
    @jwt_required()
    def get(self):
        '''
            Get course for a user through their identity
        '''
        email = get_jwt_identity()
        current_user = Student.query.filter_by(email=email).first()
        current_user_id = current_user.id
        courses = Course.query.filter_by(
            student=current_user_id).all()
        course_name = courses
        return course_name, HTTPStatus.OK


# route for setting up a student course using authorization
@course_namespace.route('/set_course')
class SetCourse(Resource):
    @course_namespace.expect(course_get_model)
    @course_namespace.marshal_with(course_get_model)
    @jwt_required()
    def post(self):
        '''
            Set up Course
        '''

        username = get_jwt_identity()
        current_user = Student.query.filter_by(email=username).first()
        current_user_id = current_user.id
        courses = Course.query.filter_by(
            student=current_user_id).all()
        course_name = courses

        data = course_namespace.payload

        set_course = Course(
            name=data['name'],
            instructor=data['instructor'],
        )

        if len(course_name) >= 1:
            return {'message': 'You are not allowed to create a course again'}, HTTPStatus.UNAUTHORIZED
        else:
            set_course.student = current_user.id

            set_course.save()

            return set_course, HTTPStatus.CREATED


# Todo: Allow access to grade from admin models and calculate GPA
# Todo: Create Admin Models
