from flask_restx import Resource, Namespace, fields
from flask import request
import json

from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from ..models.student import Student
from ..models.grades import Grade
from ..models.admin import Admin

grading_namespace = Namespace(
    'grading', description="Admin Grading for student")

grading_schema = grading_namespace.model('Grading', {
    'id': fields.Integer(),
    'score': fields.String(required=True, description='GPA grading for students')
})


# setting grade for student through admin
@grading_namespace.route('/grade/student/<int:student_id>')
class GradeStudentById(Resource):
    @grading_namespace.expect(grading_schema)
    @grading_namespace.marshal_with(grading_schema)
    @jwt_required()
    def post(self, student_id):
        '''
            Grading for Students By Id
        '''

        user_allowed = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=user_allowed).first()
        author_student = Student.query.filter_by(email=user_allowed).first()
        data = request.get_json()
        user_id = Student.query.filter_by(id=student_id).first()
        user_id_id = user_id.id
        grades = Grade.query.filter_by(student=user_id_id).all()
        try:
            if len(grades) >= 1:
                return {'message': 'You are not allowed to grade this student again'}, HTTPStatus.UNAUTHORIZED
            else:
                if author_admin:
                    set_grade = Grade(score=data['score'])
                    set_grade.student = user_id_id
                    print(set_grade.student)
                    set_grade.save()
                    return set_grade, HTTPStatus.CREATED
                elif author_student:
                    return {"message": "UNAUTHORIZED"}, HTTPStatus.UNAUTHORIZED
        except AttributeError:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND


# get grades of student through id
@grading_namespace.route('/grade/student')
class GetGradeOfStudent(Resource):
    @grading_namespace.marshal_with(grading_schema)
    @jwt_required()
    def get(self):
        '''
            Get Grades of Students by the student
        '''
        user_allowed = get_jwt_identity()
        user_id = Student.query.filter_by(email=user_allowed).first()
        user_id_grade = user_id.grade

        return user_id_grade, HTTPStatus.OK
