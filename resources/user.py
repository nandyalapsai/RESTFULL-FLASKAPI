import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class Register(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,help="username cannot be empty")
    parser.add_argument('password',type=str,required=True,help="password cannot be empty")


    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message":f"username {data['username']} already exists"},400
        else:
            user = UserModel(**data)
            user.save_user()
            return {"message":"user created successfully"}