from cache import cache
from flask_restful import Api
from tmodel import db,User,Role,tracker
from flask import Flask
from tapi import TrackerAPI,LoggerAPI,UserAPI,Export,Export_Log
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore, Security,auth_required, current_user,hash_password
from jinja2 import Template
from mela import send_email
import workers 
from task import pdf_report

app = Flask(__name__)
app.secret_key = "thisisasecertkey"
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'thisisasecretsalt'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 100


api = Api(app)
CORS(app)
db.init_app(app)
cache.init_app(app)

# WTF_CSRF_ENABLED = False not to use like this..waste two days find the solution for this.

api.add_resource(UserAPI,"/api/user","/api/user/<string:email>")
api.add_resource(TrackerAPI,"/api/tracker","/api/tracker/<string:email>","/api/tracker/<string:email>/<int:id>")
# api.add_resource(LoggerAPI,"/api/log","/api/log/<string:user_name>/<int:tracker_id>/<int:log_id>")
api.add_resource(LoggerAPI,"/api/log","/api/log/<int:tracker_id>/<int:log_id>","/api/log/<string:type>/<int:id>")
api.add_resource(Export,"/api/export","/api/export/tracker/<string:email>")
api.add_resource(Export_Log,"/api/csv","/api/csv/<string:email>/<int:tracker_id>")


celery = workers.celery
app.app_context().push()

celery.conf.update(
     broker_url='redis://localhost:6379/1',
     result_backend='redis://localhost:6379/2'
 )

celery.Task = workers.ContextTask
app.app_context().push()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="shrikrishnapandey72+1@gmail.com"):
        user_datastore.create_user(email="shrikrishnapandey72+1@gmail.com",username="sk",password=hash_password("passyo"))
    db.session.commit()  

@celery.task()
def monthly_reminder():
    user_details =User.query.all()
    user_email_list =[]
    data =[]
    u_list =[]
    
    for userr in user_details :
        # print(userr.email)
        user_email_list.append(userr.email)
        user = User.query.filter_by(email = userr.email).first()
        username = user.username
        u_list.append(username)
        tracks  = user.trackers
        tracker_ids = []
        for i in tracks:
            # print(i.id)
            tracker_ids.append(i.id)
        details = []    
        for j in tracker_ids:    
            detail = tracker.query.filter_by(id=j).first()
            details.append(detail)
            print(detail.name)
        count = 0  
        t = []
        # d = {}  
        for k in details:
            count+=1
            track_dict = {"id":count ,"Tracker_name":k.name,"Tracker_Description":k.description,"Tracker_Type":k.tracker_type, "Setting": k.setting , "date_created": str(k.date_created) }
            # d[count]=track_dict
            t.append(track_dict)
        pdf_report(t,username)

        with open('./templates/report.html','r') as f:
            template = Template(f.read())
        send_email(userr.email,'Monthly Pdf Report',template.render(User=username,data=t),content="html",attachment="./"+str(username)+"_tracK_Karoo.pdf")    
    data.append(t)
    return "u_list,data,user_email_list"    
   
def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)

@celery.task()
def daily_reminder_func():
    user_details =User.query.all()
   
    for userr in user_details :
        # print(userr.email)
        email = userr.email
        user = User.query.filter_by(email = userr.email).first()
        username = user.username
        
        with open('./templates/daily_reminder.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username),content="html")
    return "Daily reminder sent"

from celery.schedules import crontab
import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Calcutta')) 


@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    # sender.add_periodic_task(30.0,monthly_reminder.s(),name="at 30 sec")
    # sender.add_periodic_task(20.0,daily_reminder_func.s(),name="at 20 sec")
    sender.add_periodic_task(
        crontab(hour=17, minute=30, day_of_month="1",nowfun=timee),
        monthly_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(hour=1, minute=40, day_of_week="*",nowfun=timee),
        daily_reminder_func.s(),
    )

if __name__ == "__main__":
    app.run(debug=True)
# celery -A tapp.celery worker -l info
# celery -A tapp.celery beat --max-interval 1 -l info
# mailhog
# python3 tapp.py
# npm run serve
# redis-server
