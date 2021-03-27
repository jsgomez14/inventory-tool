from app import app
from flask import request
from flask_pymongo import PyMongo
import os
from datetime import datetime,timezone 

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

entries = mongo.db.entry
outs = mongo.db.out
products = mongo.db.product
providers = mongo.db.provider
stocks_summary = mongo.db.stock_summary

def parse_providers(data):
    return [{'id' : rec['id'], 'name' : rec['name']} for rec in data]

def parse_products(data):
    return [{'id' : rec['id'], 'name' : rec['name'],"provider_id": rec["provider_id"],'description' : rec['description'],'measure' : rec['measure']} for rec in data]

def parse_entries(data):
    return [{'provider_id':rec["provider_id"],'provider_name':rec["provider"]["name"],'product_id':rec["product_id"],'product_name':rec["product"]["name"],'quantity':rec["quantity"],'created_at':rec["created_at"].strftime("%Y-%m-%d %H:%M:%S")} for rec in data]

def parse_outs(data):
    return [{'provider_id':rec["provider_id"],'provider_name':rec["provider"]["name"],'product_id':rec["product_id"],'product_name':rec["product"]["name"],'quantity':rec["quantity"],'value' :rec['value'],'created_at':rec["created_at"].strftime("%Y-%m-%d %H:%M:%S")} for rec in data]

def parse_stocks_summary(data):
    resp = None
    try:
        resp= [{'product_id':rec["product_id"],'product_name':rec["product"]["name"], 'provider_id':rec["product"]["provider_id"],'provider_name':rec["provider"]["name"],'stock':rec["stock"], 'created_at':rec["created_at"].strftime("%Y-%m-%d %H:%M:%S"),'updated_at':rec["updated_at"].strftime("%Y-%m-%d %H:%M:%S")} for rec in data]
    except:
        resp=[{'product_id':rec["product_id"], 'stock':rec["stock"], 'created_at':rec["created_at"].strftime("%Y-%m-%d %H:%M:%S"),'updated_at':rec["updated_at"].strftime("%Y-%m-%d %H:%M:%S")} for rec in data]
    return resp


def parse_stocks_summary2(data):
    return [{'product_id':rec["product_id"], 'stock':rec["stock"], 'created_at':rec["created_at"].strftime("%Y-%m-%d %H:%M:%S"),'updated_at':rec["updated_at"].strftime("%Y-%m-%d %H:%M:%S")} for rec in data]


@app.route('/')
def index():
    return "Welcome to the inventory API!!"

@app.route('/product', methods=["GET"])
def get_products():
    product_id = request.args.get('id')
    resp = None
    if product_id:
        resp = {'result': parse_products(products.find({'id': int(product_id)}))}
    return {'result': parse_products(products.find())} if resp is None else resp

@app.route('/provider', methods=["GET"])
def get_providers():
    provider_id = request.args.get('id')
    resp = None
    if provider_id:
        resp = {'result': parse_providers(providers.find({'id': int(provider_id)}))}
    return {'result':parse_providers(providers.find())} if resp is None else resp

@app.route('/entry', methods=["GET"])
def get_entries():
    pipeline = [{'$lookup': 
                {'from' : 'product',
                 'localField' : 'product_id',
                 'foreignField' : 'id',
                 'as' : 'product'}},
                {'$unwind':"$product" },
                {
                    '$lookup':{
                        'from': "provider", 
                        'localField': "provider_id", 
                        'foreignField': "id",
                        'as': "provider"
                    }
                },
                {'$unwind':"$provider"},
             ]
    return {'result' : parse_entries(entries.aggregate(pipeline))}

@app.route('/out', methods=["GET"])
def get_outs():
    pipeline = [{'$lookup': 
                {'from' : 'product',
                 'localField' : 'product_id',
                 'foreignField' : 'id',
                 'as' : 'product'}},
                {'$unwind':"$product" },
                {
                    '$lookup':{
                        'from': "provider", 
                        'localField': "provider_id", 
                        'foreignField': "id",
                        'as': "provider"
                    }
                },
                {'$unwind':"$provider"},
             ]
    return {'result' : parse_outs(outs.aggregate(pipeline))}

@app.route('/stock_summary', methods=["GET"])
def get_stocks_summary():
    pipeline = [{'$lookup': 
                {'from' : 'product',
                 'localField' : 'product_id',
                 'foreignField' : 'id',
                 'as' : 'product'}},
                {'$unwind':"$product" },
                {
                    '$lookup':{
                        'from': "provider", 
                        'localField': "product.provider_id", 
                        'foreignField': "id",
                        'as': "provider"
                    }
                },
                {'$unwind':"$provider"},
             ]
    return {'result' : parse_stocks_summary(stocks_summary.aggregate(pipeline))}

@app.route('/entry', methods=["POST"])
def create_entry():
    result =None
    is_new_prov = False
    new_entry = request.get_json()
    print(" New Entry: ",new_entry)
    new_provider = {'id': new_entry["provider_id"], 'name': new_entry["provider_name"]}
    new_product = {'id': new_entry["product_id"],"name":new_entry["product_name"],"provider_id": new_entry["provider_id"],"description":new_entry["product_description"],"measure":new_entry["measure"]}

    provider = parse_providers(providers.find({'id': new_entry["provider_id"]}))
    print("PROVIDER: ",provider)
    if not provider:
        is_new_prov = True
        result= {'result' : "New provider, product and entry have been created succesfully."}
        providers.insert_one(new_provider)
    product = parse_products(products.find({'id': new_entry["product_id"]}))
    if not product:
        if not is_new_prov:
            result = {'result': provider[0]["name"]+ " has a new product. Entry created succesfully"}
        products.insert_one(new_product)
    
    utc_datetime = datetime.strptime(new_entry['entry_date'], '%Y-%m-%d %H:%M:%S')

    entry = {'provider_id':new_entry["provider_id"],'product_id':new_entry["product_id"],'quantity':new_entry["quantity"],'created_at':utc_datetime}
    entries.insert_one(entry)
    stock_summary = parse_stocks_summary2(stocks_summary.find({'product_id': new_entry["product_id"]}))
    print("Stock Summary: ", stock_summary)
    if stock_summary:
        stocks_summary.update_one({'product_id': new_entry["product_id"]},{"$set": {'stock' : stock_summary[0]["stock"]+new_entry["quantity"], 'updated_at': utc_datetime}})
    else:
        stocks_summary.insert_one({'product_id': new_entry["product_id"],'stock': new_entry["quantity"],'created_at':utc_datetime,'updated_at':utc_datetime})
    return result if result is not None else {'result': 'Entry created succesfully'}

@app.route('/out', methods=["POST"])
def create_out():
    result =None
    new_out = request.get_json()
    print(new_out)
    provider = parse_providers(providers.find({'id': new_out["provider_id"]}))
    product = parse_products(products.find({'id': new_out["product_id"]}))
    stock_summary = parse_stocks_summary2(stocks_summary.find({'product_id': new_out["product_id"]}))
    utc_datetime = datetime.strptime(new_out['out_date'], '%Y-%m-%d %H:%M:%S')
    
    if provider and product and stock_summary:
        if stock_summary[0]["stock"]-new_out["quantity"] >= 0:
            out = {'provider_id':new_out["provider_id"],'product_id':new_out["product_id"],'quantity':new_out["quantity"],'value':new_out["value"],'created_at':utc_datetime}
            outs.insert_one(out)
            stocks_summary.update_one({'product_id': new_out["product_id"]},{"$set": {'stock' : stock_summary[0]["stock"]-new_out["quantity"], 'updated_at': utc_datetime}})
            result = {"result": "out has been created succesfully."}
        else:
            result = {"result": "ERROR1: OUT is exceding the actual stock."}
    else:
        result = {"result": "ERROR2: Provider/Product does not exist."}
    return result

