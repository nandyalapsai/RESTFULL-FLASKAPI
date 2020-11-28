from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import Authenticate,identity
from resources.user import Register
from resources.items import Item,ItemList
from resources.store import StoreList,Store


app = Flask(__name__)
app.secret_key = "nandu_nandhyala"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWT(app,Authenticate,identity)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item,"/item/<name>")
api.add_resource(Store,"/store/<name>")
api.add_resource(ItemList,"/items")
api.add_resource(Register,"/register")
api.add_resource(StoreList,"/stores")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

print("sample flask app..")