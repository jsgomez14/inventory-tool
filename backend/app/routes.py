from app import app
from flask import request
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb+srv://admin:Inventory2021*@cluster0.sykxj.mongodb.net/inventory?retryWrites=true&w=majority"
mongo = PyMongo(app)

entries = mongo.db.entry
products = mongo.db.product
providers = mongo.db.provider

def parse_providers(data):
    return [{'id' : rec['id'], 'name' : rec['name']} for rec in data]

def parse_products(data):
    return [{'id' : rec['id'], 'name' : rec['name'],"provider_id": rec["provider_id"],'description' : rec['description'],'measure' : rec['measure']} for rec in data]

def parse_entries(data):
    return [{'provider_id':rec["provider_id"],'product_id':rec["product_id"],'quantity':rec["quantity"]} for rec in data]

@app.route('/')
def index():
    return "Welcome to the inventory API!!"

@app.route('/product', methods=["GET"])
def get_products():
    return {'result': parse_products(products.find())}

@app.route('/provider', methods=["GET"])
def get_providers():
    return {'result':parse_providers(providers.find())}

@app.route('/entry', methods=["GET"])
def get_entries():
    return {'result' : parse_entries(entries.find())}

@app.route('/entry', methods=["POST"])
def create_entry():
    result =None
    is_new_prov = False
    new_entry = request.get_json()
    new_provider = {'id': new_entry["provider_id"], 'name': new_entry["provider_name"]}
    new_product = {'id': new_entry["product_id"],"name":new_entry["product_name"],"provider_id": new_entry["provider_id"],"description":new_entry["product_description"],"measure":new_entry["measure"]}

    provider = parse_providers(providers.find({'id': new_entry["provider_id"]}))
    if not provider:
        is_new_prov = True
        result= {'result' : "New provider, product and entry have been created succesfully."}
        providers.insert_one(new_provider)
    filter = {'id': new_entry["product_id"]}
    product = parse_products(products.find(filter))
    if not product:
        if not is_new_prov:
            result = {'result': provider[0]["name"]+ " has a new product. Entry created succesfully"}
        products.insert_one(new_product)
        
    entry = {'provider_id':new_entry["provider_id"],'product_id':new_entry["product_id"],'quantity':new_entry["quantity"]}
    entries.insert_one(entry)
    return result if result is not None else {'result': 'Entry created succesfully'}