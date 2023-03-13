# This path is meant for admins only to delete students
# and student course by from database

from flask_restx import Resource, Namespace, abort
from ..models.student import Student
from ..models.admin import Admin
from ..models.course import Course
from flask import jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db


admin_namespace = Namespace(
    'auth', description="Admin authentication for deleting  student on the management api")


@admin_namespace.route('/delete/<int:id>')
class DeleteStudentById(Resource):
    @jwt_required()
    def delete(self, id):
        '''
            Delete Student by id
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()
        if author_admin:
            student = Student.query.filter_by(id=id).first()
            student.delete_by_id(id)
            return {"message": "Student deleted successfully"}, HTTPStatus.OK
        if author_student:
            return {"message": "You are not authorized to delete student"}, HTTPStatus.UNAUTHORIZED


@admin_namespace.route('/student/<int:student_id>/course')
class DeleteStudentCourse(Resource):
    @jwt_required()
    def delete(self, student_id):
        '''
            Delete Course for a Student By Admin
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()

        student_id = Student.query.filter_by(id=student_id).first()
        current_user_id = student_id.id
        course_id = Course.query.filter_by(student=current_user_id).first()
        course_id_id = course_id.id

        print(course_id_id)
        if author_admin:
            if student_id:
                # students_id_course = students_id.student
                db.session.delete(course_id)
                db.session.commit()

            return {'message': f'Course deleted for student {student_id}'}, HTTPStatus.ACCEPTED
        elif author_student:
            return {"message": "UNAUTHORIZED"}, HTTPStatus.UNAUTHORIZED


#get amount of student registered in one course
@admin_namespace.route('/course/<string:course_name>/students')
class GetStudentPerCourse(Resource):
    @jwt_required()
    def get(self, course_name):
        '''
            Get student registered in each course
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()
        course = Course.query.filter_by(name=course_name)
        if author_admin:
            for courses in course:
                course_student = courses.student
            if course:
                return {'students': course_student}, HTTPStatus.OK
        elif author_student:
            return {'message': 'You are not authorized'}, HTTPStatus.UNAUTHORIZED
