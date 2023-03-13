from flask_restx import Resource, Namespace, fields
from ..models.student import Student
from ..models.admin import Admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

student_namespace = Namespace(
    'views', description="Authentication for student management api")

student_model = student_namespace.model('Students', {
    'id': fields.Integer(readOnly=True, description='Student Indentifier'),
    'name': fields.String(required=True, description='Student name'),
    'email': fields.String(required=True, description='Student email address'),
    'password': fields.String(required=True, description='Student password')
})


@student_namespace.route('/getallstudent')
class GetAllStudent(Resource):
    @student_namespace.marshal_with(student_model)
    @jwt_required()
    def get(self):
        '''
            Get All Student
        '''
        current_user = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=current_user).first()
        author_student = Student.query.filter_by(email=current_user).first()
        if author_admin:
            students = Student.query.all()
            return students, HTTPStatus.OK
        if author_student:
            return {"message": "You are not authorized to view all students"}, HTTPStatus.UNAUTHORIZED
