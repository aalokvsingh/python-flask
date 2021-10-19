from flask import Flask
import config
# from database import db


#mysql import and create mysql object
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO
app.config['SECRET_KEY'] = config.SECRET_KEY
db = SQLAlchemy(app)
db.init_app(app)



print("alok:",config.APP_ROOT)

from user.view import user_blp
app.register_blueprint(user_blp)

from product.view import product_blp
app.register_blueprint(product_blp)


@app.route('/', methods=['GET', 'POST'])
def hellojson():
    userData = {'username':'1alok5n','firstname':'Alok Singh'}
    return userData

if __name__ == '__main__':
    app.run()
