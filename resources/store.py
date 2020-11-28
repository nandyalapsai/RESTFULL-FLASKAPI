from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_store(name)
        if store:
            return store.json()
        else:
            return {"message":"store not found"},404

    def post(self,name):
        store = StoreModel.find_store(name)
        if store:
            return {"message":"store already present"},400
        else:
            store = StoreModel(None,name)
            store.save_to_db()
            return store.json(),201
    
    def delete(self,name):
        store = StoreModel.find_store(name)
        if store:
            store.delete_store()
            return {"message":"item deleted successfully"},200
        else:
            return {"message":"store not found"},404


class StoreList(Resource):
    def get(self):
        stores = [ store.json() for store in StoreModel.query.all()]
        return {"stores":stores}
