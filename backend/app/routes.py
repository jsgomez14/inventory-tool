from app import app
from flask import request
from flask_pymongo import PyMongo
import os
from datetime import datetime,timezone 

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

entries = mongo.db.entry
products = mongo.db.product
providers = mongo.db.provider
stocks_summary = mongo.db.stock_summary

def parse_providers(data):
    return [{'id' : rec['id'], 'name' : rec['name']} for rec in data]

def parse_products(data):
    return [{'id' : rec['id'], 'name' : rec['name'],"provider_id": rec["provider_id"],'description' : rec['description'],'measure' : rec['measure']} for rec in data]

def parse_entries(data):
    return [{'provider_id':rec["provider_id"],'product_id':rec["product_id"],'quantity':rec["quantity"],'created_at':rec["created_at"]} for rec in data]

def parse_stocks_summary(data):
    return [{'product_id':rec["product_id"],'stock':rec["stock"], 'created_at':rec["created_at"],'updated_at':rec["updated_at"]} for rec in data]

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

@app.route('/stock_summary', methods=["GET"])
def get_stocks_summary():
    return {'result' : parse_stocks_summary(stocks_summary.find())}

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

    curr_time = datetime.now(tz=timezone.utc)
    entry = {'provider_id':new_entry["provider_id"],'product_id':new_entry["product_id"],'quantity':new_entry["quantity"],'created_at':curr_time}
    entries.insert_one(entry)
    stock_summary = parse_stocks_summary(stocks_summary.find({'product_id': new_entry["product_id"]}))
    curr_time = datetime.now(tz=timezone.utc)
    if stock_summary:
        stocks_summary.update_one({'product_id': new_entry["product_id"]},{"$set": {'stock' : stock_summary[0]["stock"]+new_entry["quantity"], 'updated_at': curr_time}})
    else:
        stocks_summary.insert_one({'product_id': new_entry["product_id"],'stock': new_entry["quantity"],'created_at':curr_time,'updated_at':curr_time})
    return result if result is not None else {'result': 'Entry created succesfully'}

