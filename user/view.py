from flask import Blueprint, json,jsonify,request,make_response
import database as db
import logging
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from functools import wraps
from user.model import User
from config import SECRET_KEY
# from .. import app
import datetime

user_blp = Blueprint('user_blp','__name__',url_prefix='/user')

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # current_user =''
        if 'x-api-key' in request.headers:
            token = request.headers['x-api-key']
            # return token
        # return token
        if not token:
            return make_response(jsonify({'status':False,"data":[],'message':'a valid token is missing'}),200)
        # return token
        try:
            # return token
            # data = jwt.decode(token, app.config['SECRET_KEY'])
            data = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            # return data
            current_user = User.query.filter_by(username=data['username']).first()
            # return current_user.username
        except Exception as e:
           return make_response(jsonify({'status':False,"data":[e],'message':'token is invalid!'}),200)

        return f(current_user, *args, **kwargs)

    return decorator 


@user_blp.route('/login',methods=['POST'])
def login():
    
    auth = request.authorization 
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})  
    
    UserData = User.query.filter_by(username=auth.username).first()
    if UserData:
        verify_password = check_password_hash(UserData.password_hash,auth.password)
    # return str(verify_password)
    if UserData and verify_password:
        # return(jsonify([UserData.lastname,UserData.firstname,UserData.id]))
        # generates the JWT Token
        token = jwt.encode({
            'username': UserData.username,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
        },SECRET_KEY,'HS256')
        # return token
        return make_response(
            jsonify({'status':True,'data':[token],'message':'authentication successfull'}),
            201
        )
    else:
        return make_response(
            jsonify({'status':False,'data':[],'message':'User not found'}),
            201
        )
    

@user_blp.route('/<int:id>',methods=['GET','POST'])
@user_blp.route('/',methods=['GET','POST'])
@token_required
def getuser(id=None):
    # return 'alok'
    try:
        fields = 'id,username,name,role,status,email'
        where =''
        if id:
            where = ' and id={}'.format(id)
        query ="SELECT {0} FROM USER where status= {1} {2}".format(fields,1,where)
        rows = db.executeSelectQuery(query)
        logging.debug(query)
        logging.debug("Result {}".format(rows))
        return jsonify(rows)
    except Exception as e:
        return jsonify(str(e))


@user_blp.route('/register',methods=['POST'])
def register_user():
    try:
        username    = request.form.get('username')
        name        = request.form.get('name')
        username    = request.form.get('username')
        email       = request.form.get('email')
        role        = request.form.get('role')
        status      = request.form.get('status')
        password    = request.form.get('password')
        password_hash = generate_password_hash(password,method='sha256') if password else None

        username_re = User.query.filter_by(username = username).first()
        email_re = User.query.filter_by(email = email).first()

        if not username_re and not email_re:
            query ="INSERT INTO user (username,name,email,role,status,password,password_hash) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(username,name,email,role,status,password,password_hash)
            # return query
            # return "A: {}".format(query)
            rows = db.executeInsertQuery(query)
            logging.debug(query)
            logging.debug("Last inserted id {}".format(rows))
            return jsonify(rows)
        else:
            return make_response('User already exists. Please Log in.', 202)
    except Exception as e:
        return jsonify(str(e))

@user_blp.route('delete/<int:id>',methods=['DELETE'])
@token_required
def delete_user(self,id):
    try:
        table = 'user'
        where = " id = {}".format(id)
        query = "DELETE FROM {0} where {1}".format(table,where)
        rows = db.executeQuery(query)
        logging.debug(query)
        logging.debug("No of row deleted {}".format(rows))
        return jsonify(rows)
    except Exception as e:
        return jsonify(str(e))

@user_blp.route('update/<int:id>',methods=['PATCH'])
@token_required
def update_user(id):
    try:
        username    = request.form.get('username')
        name        = request.form.get('name')
        username    = request.form.get('username')
        email       = request.form.get('email')
        role        = request.form.get('role')
        status      = request.form.get('status')
        password    = request.form.get('password')
        fields = "role={0},status={1}".format(role,status)
        where  =" id={}".format(id)
        query = "UPDATE user set {0} where {1}".format(fields,where)
        rows = db.executeQuery(query)
        logging.debug(query)
        logging.debug("No of row affected {}".format(rows))
        return jsonify(rows)
    except Exception as e:
        return jsonify(str(e))




            
        


