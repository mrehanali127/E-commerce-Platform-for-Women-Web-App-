import re
from flask import *
from flask_sqlalchemy import SQLAlchemy
#from werkzeug.security import check_password_hash,generate_password_hash

#from flask_mysqldb import MySQL

from Rehan_web import app,photos
from .models import User,db,Category,Product

###  configuration
#app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# default route
@app.route('/',methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        email1 = request.form.get('email')
        password1 = request.form.get('password')

        #If user have not entered Email or Password
        if not email1 or not password1:
            flash('Kindly fill all fields in form')
            return redirect(url_for('login_page'))

        # Is user exist in out database
        log_user=User.query.filter_by(email=email1).first()
        if log_user:
            #if check_password_hash(log_user.password,password1):
            if log_user.password==password1:
                current_user=log_user.firstName
                session['current_user']=current_user
                session['user_email']=email1
                session['user_available']=True
                if not log_user.skill:
                    return redirect(url_for('home_client'))
                else:
                    return redirect(url_for('home_artist'))
            else:
                flash("Your Password is Incorrect")
                return redirect(url_for('login_page'))
        else:
            flash("Entered email is not registered")
            return redirect(url_for('login_page'))


        #return redirect(url_for('register'))

    return render_template('login_page.html')




@app.route('/register',methods=['GET', 'POST'])
def register():
    return render_template('register.html')



@app.route('/register_artist',methods=['GET','POST'])
def register_artist():
    return render_template('register_artist.html')



@app.route('/register_client',methods=['GET','POST'])
def register_client():
    return render_template('register_client.html')



@app.route('/registration', methods=["POST"])
def registration():
    fname=request.form.get('fname')
    lname=request.form.get('lname')
    mail=request.form.get('mail')
    phone=request.form.get('phone')
    password=request.form.get('password')
    city=request.form.get('city')
    province=request.form.get('state')
    gender=request.form.get('gender')
    skill=request.form.get('skill')

    #enc_password=generate_password_hash(password)
    enc_password=password

    if validate_email(mail) is False:
        if not skill:
            flash("Email Already Exists")
            return redirect(url_for('register_client'))
        if skill:
            flash("Email Already Exists")
            return redirect(url_for('register_artist'))
    

    if validate_phone(phone) is False:
        if not skill:
            flash("Entered Phone Number is already registered")
            return redirect(url_for('register_client'))
        if skill:
            flash("Entered Phone Number is already registered")
            return redirect(url_for('register_artist'))



    new_user=User(mail,fname,lname,phone,enc_password,city,province,gender,skill)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_page'))


@app.route('/home_client')
def home_client():
    products=Product.query.all()
    return render_template('index_client.html',products=products)



@app.route('/home_artist')
def home_artist():
    products=Product.query.all()
    return render_template('index_artist.html',products=products)
    


@app.route('/specific_category/<string:category>')
def specific_category(category):
    selected_category=Category.query.filter_by(categoryName=category).first()
    products=Product.query.filter_by(category_id=selected_category.id).all()
    return redirect(url_for('home_client',products=products))



@app.route('/goForAdd')
def goForAdd():
    return render_template('add_product.html')

@app.route('/addProduct', methods=["POST"] )
def addProduct():
    p_id=request.form.get('product_id')
    p_name=request.form.get('product_name')
    category=request.form.get('product_category')
    p_description=request.form.get('product_description')
    p_price=request.form.get('product_price')
    #p_artist=session['current_user']

    new_image=photos.save(request.files.get('filebutton'))
    
    new_product=Product(p_id,p_name,p_price,p_description,new_image,category,session['user_email'])
    db.session.add(new_product)
    db.session.commit()

    return "PRoduct Inserted"


@app.route('/editProduct/<int:product_id>',methods=["GET","POSt"])
def editProduct(product_id):
    product=Product.query.get(product_id)
    return render_template('editProduct.html',product=product)



@app.route('/deleteProduct/<int:product_id>',methods=['GET','POST'])
def deleteProduct(product_id):
    del_product=Product.query.get(product_id)
    if del_product:
        db.session.delete(del_product)
        db.session.commit()
    return redirect(url_for('home_artist'))
    

@app.route('/logout')
def logout():
    session.clear()
    session['user_available']=True

    return redirect(url_for('login_page'))






def validate_email(mail):
    user_email=User.query.filter_by(email=mail).first()
    if user_email:
        return False
    else:
        return True

def validate_phone(mobile_phone):
    user_phone=User.query.filter_by(phoneNo=mobile_phone).first()
    if user_phone:
        return False
    else:
        return True





