import sqlite3
from flask import request,jsonify
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="price field is missing")
    parser.add_argument('store_id',type=int,required=True,help="storeid field is missing")
    
    # @jwt_required()
    def get(self,name):
        item = None
        try:
            item = ItemModel.find_item(name).json()
            #returns None if no item found
            print(item)
        except:
            return {"message":"error occured while getting item"},500
        else:
            if item:
                return {"item":item},200
            return {"message":"item not found"},404

    def post(self,name):
        data = self.parser.parse_args()
        item = ItemModel.find_item(name)
        if item:
            return {"message":"item already exists"},400
        else:
            item = ItemModel(None,name,**data)

            try:
                item.save_to_db()
            except:
                return {"message":"error occured during item insertion"}
            
            return item.json(),201

    def put(self,name):
        #excepts price  everything gets removed from the payload while parsing
        # data = request.get_json()
        data = self.parser.parse_args()
        item = ItemModel.find_item(name)
        status = None
        if item:
            item.price = data["price"]
            status = "updated"
        else:
            item = ItemModel(None,name,**data)
            status = "inserted"
        try:
            item.save_to_db()
        except:
            return {"message":"error occured.."}    
        print(status)
        return (item.json(),201) if status=="inserted" else {"message":f"item {name} updated.."}

    def delete(self,name):
        item = ItemModel.find_item(name)
        if item:
            try:
                item.delete_item()
            except:
                return {"message":"error occured while deleting"}    
            return {"message":f"item {name} deleted successfully"}
        else:
            return {"message":f"item {name} not found.."}
            

class ItemList(Resource):
    # @jwt_required()
    def get(self):

        # items = list(map(lambda x: x.json(),ItemModel.quer.all())) #both are same
        items = [item.json() for item in ItemModel.query.all()]
        return {"items":items},200