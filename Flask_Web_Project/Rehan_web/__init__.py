from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
import os



basedir=os.path.abspath(os.path.dirname(__file__))
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://sql6430729:ayVh8Kw7cl@sql6.freemysqlhosting.net/sql6430729'
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(basedir,'static/images')

photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)

from Rehan_web import models
from Rehan_web import views