from flask import Blueprint, json,jsonify,request,make_response,json
import logging
from product.model import MasterProduct
import datetime
from database import db
from user.view import token_required

product_blp = Blueprint('product_blp','__name__',url_prefix='/product')

@product_blp.route('/<int:id>',methods=['GET','POST'])
@product_blp.route('/',methods=['GET','POST'])
@token_required
def getproduct(self,id=None):
    # return 'aaa'
    try:
        if id is None:
            products = MasterProduct.query.all()
        else:
            products = MasterProduct.query.filter_by(id=id).all()
        result = []
        for product in products:
            product_data = {}
            product_data['id'] = product.id
            product_data['product'] = product.product
            product_data['status'] = product.status
            product_data['parent_product_id'] = product.parent_product_id
            result.append(product_data)

        
        logging.debug("Result {}".format(result))
        response =  make_response(jsonify({"message":result}),200)
        response.headers["Content-Type"] = "application/json"
        return response
            
    except Exception as e:
        return jsonify(str(e))

@product_blp.route('/create',methods=['POST'])
@token_required
def addproduct(self):
    # return 'aaa'
    try:
        getpayload = request.get_json()
        # return str(getpayload)
        product =getpayload.get('product')
        parent_product_id =getpayload.get('parent_product_id')
        if not product:
            return make_response(jsonify({'status':False,'data':[],'message':"Product name is required"}),300)
        
        ProductData = MasterProduct(product=product,parent_product_id=parent_product_id,status=1)
        db.session.add(ProductData)
        db.session.commit()
        if ProductData.id:
            id = ProductData.id
            msg ='Product created Successfull'
        else:
            msg ='Product not created'

        logging.info(msg)
        return make_response(jsonify({'status':True,"data":[id],'message':msg}),200)
        
    except Exception as e:
        return jsonify(str(e))

@product_blp.route('/update/<int:id>',methods=['PATCH'])
@token_required
def updateproduct(self,id=None):
    # return 'aaa'
    try:
        getpayload = request.get_json()
        # return str(getpayload)
        
        productData = MasterProduct.query.get(id)
        if not productData:
            msg = 'Product not found!'
            return make_response(jsonify({'status':True,"data":[id],'message':msg}),200)
        
        product =getpayload.get('product') if getpayload.get('product') else productData.product
        parent_product_id =getpayload.get('parent_product_id') if getpayload.get('parent_product_id') else productData.parent_product_id
        status =getpayload.get('status') if getpayload.get('status') else productData.product

        productData.product =product
        productData.parent_product_id =parent_product_id
        productData.status =status
        db.session.commit()
        msg ='Product Updated !'
        logging.info(msg)
        return make_response(jsonify({'status':True,"data":[id],'message':msg}),200)
    except Exception as e:
        return jsonify(str(e))

@product_blp.route('/delete/<int:id>',methods=['DELETE'])
@token_required
def deleteproduct(self,id=None):
    # return 'aaa'
    try:
        MasterProduct1 = MasterProduct.query.filter_by(id=id).first()
        
        if not MasterProduct1:
            msg = 'Product not found!'
            return make_response(jsonify({'status':True,"data":[id],'message':msg}),200)
        
        db.session.delete(MasterProduct1)
        db.session.commit()

        msg ='Product deleted'
        logging.info(msg)
        return make_response(jsonify({'status':True,"data":[id],'message':msg}),200)

    except Exception as e:
        return jsonify(str(e))