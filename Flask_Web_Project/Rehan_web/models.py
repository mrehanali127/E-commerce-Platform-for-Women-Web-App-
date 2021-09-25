from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

from Rehan_web import app

db=SQLAlchemy(app)

class User(db.Model):
    email=db.Column(db.String(55),primary_key=True)
    firstName=db.Column(db.String(80))
    lastName=db.Column(db.String(80))
    phoneNo=db.Column(db.String(11))
    password=db.Column(db.String(255))
    city=db.Column(db.String(80))
    province=db.Column(db.String(80))
    gender=db.Column(db.String(80))
    skill=db.Column(db.String(80))
    
    def __init__(self,email,firstName,lastName,
        phoneNo,password,city,province,gender,skill):

        self.email=email;
        self.firstName=firstName;
        self.lastName=lastName;
        self.phoneNo=phoneNo;
        self.password=password;
        self.city=city;
        self.province=province;
        self.gender=gender;
        self.skill=skill;


class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    categoryName=db.Column(db.String(80))

    def __init__(self,categoryName):
        self.categoryName=categoryName

class Product(db.Model):
    product_id=db.Column(db.String(55),primary_key=True)
    product_name=db.Column(db.Text,nullable=False)
    product_price=db.Column(db.Numeric(10,2),nullable=False)
    product_description=db.Column(db.Text,nullable=False)

    product_image=db.Column(db.String(255),nullable=False)

    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category=db.relationship('Category',backref=db.backref('categories',lazy=True))

    artist_id=db.Column(db.String(55),db.ForeignKey('user.email'),nullable=False)
    artist=db.relationship('User',backref=db.backref('users',lazy=True))

    def __init__(self,product_id,product_name,product_price,product_description,
                product_image,category_id,artist_id):
        
        self.product_id=product_id
        self.product_name=product_name
        self.product_price=product_price
        self.product_description=product_description
        self.product_image=product_image
        self.category_id=category_id
        self.artist_id=artist_id



db.create_all()








