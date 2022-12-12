from flask import jsonify
from flask_restful import Resource,Api,marshal_with,reqparse,fields
from cache import cache
from tmodel import db,tracker,User as user_model,logs,Role
import matplotlib.pyplot as plt
from flask_security import auth_required,current_user,hash_password,SQLAlchemyUserDatastore,Security
import task

user_datastore = SQLAlchemyUserDatastore(db, user_model, Role)
security = Security(user_datastore)

user_req_args = reqparse.RequestParser()
user_req_args.add_argument('username',required=True,help="username required")
user_req_args.add_argument('email',required=True,help="email required")
user_req_args.add_argument('password',required=True,help="pass required")


tracker_post_args = reqparse.RequestParser()
tracker_post_args.add_argument('Tracker_name',required=True,help="tracker name required")
tracker_post_args.add_argument('Tracker_Description')
tracker_post_args.add_argument('Tracker_Type',required=True,help="tracker type required")
tracker_post_args.add_argument('email',required=True,help="email required")
tracker_post_args.add_argument('id')
tracker_post_args.add_argument('Setting')

# logger_post_args = reqparse.RequestParser()
# logger_post_args.add_argument('user_name')

numeric_post_args = reqparse.RequestParser()
numeric_post_args.add_argument('Value',required=True,help="Value is required")
numeric_post_args.add_argument('Note')
numeric_post_args.add_argument('email')

multiple_post_args = reqparse.RequestParser()
multiple_post_args.add_argument('Value',required=True,help="Value is required")
multiple_post_args.add_argument('Note')
multiple_post_args.add_argument('email')

boolean_post_args = reqparse.RequestParser()
boolean_post_args.add_argument('Value',required=True,help="Value is required")
boolean_post_args.add_argument('Note')
boolean_post_args.add_argument('email')



user_fields = {
    'username' : fields.String ,
    'email' : fields.String ,
    # 'password' : fields.String
}

class UserAPI(Resource):
    @auth_required('token')
    @marshal_with(user_fields)
    def get(self):
        return current_user

    @marshal_with(user_fields)
    def post(self):
        args = user_req_args.parse_args()
        
        email = args.get("email")
        user_name = args.get("username")
        passw = args.get("password")
        check=user_model.query.filter_by(email=email).first()
        if check:
           return jsonify('email you entered already belongs to an account. Try another email.')
        else:
            # If user does not exists check these
            if user_name != "":
                if email:
                    if passw:
                        
                        user_datastore.create_user(email=email,username=user_name,password=hash_password(passw))
                        
                        db.session.commit()
                        data = user_model.query.filter_by(email=email).first()
                       
                        return data,200
                        
                    else:
                        return jsonify('Password cannot be empty. Please enter a valid Password')
                else:
                    return jsonify('email cannot be empty. Please Enter email')
            else:
                return jsonify('Name cannot be empty. Please enter a valid name')

tracker_fields = {
    "email" : fields.String,
    "Tracker_name" : fields.String,
    "Tracker_Description" : fields.String,
    "Tracker_Type" : fields.String,
    "setting" : fields.String
}


class TrackerAPI(Resource):

    @auth_required('token')
    @cache.memoize(timeout=40)
    def get(self,email):
        try:
            user = user_model.query.filter_by(email=email).first()
            tracks  = user.trackers
            
            tracker_ids = []
            for i in tracks:
                # print(i.id)
                tracker_ids.append(i.id)
            # print(tracker_ids," 1 ")    
            details = []    
            for j in tracker_ids:    
                detail = tracker.query.filter_by(id=j).first()
                details.append(detail)
                # print(detail.name)

            # print(details, " 2 ")    
            count = 0  
            d = {}  
            for k in details:
                count+=1
                track_dict = {"id":k.id ,"Tracker_name":k.name,"Tracker_Description":k.description,"Tracker_Type":k.tracker_type, "Setting": k.setting , "date_created": str(k.date_created) }
                d[count]=track_dict
                
            # print(d," 3 ") 
            return jsonify(d)
            
        except:    
            return jsonify({"error" :"There are some wrong user details filled and asked for."})


    @auth_required('token')
    def post(self,email):
        agrs = tracker_post_args.parse_args()
        # print(agrs)
        # print(type(agrs))
        User = email
        Name=agrs.get("Tracker_name")
        Description=agrs.get('Tracker_Description',None)
        Tracker_type=agrs.get( 'Tracker_Type',None)
        setting = agrs.get('Setting')
        # check = tracker.query.filter_by(name=Name).first()
        # user = user_model.query.filter_by(email=email).first()

        # detail = tracker.query.filter_by(name=Name,id=user.user_id).first()
        # if detail:
        #     str = "Tracker already exists."
        #     return jsonify(str)
            
        # else:    
        new_tracker=tracker(name=Name, description=Description, tracker_type=Tracker_type,setting=setting)
        user = user_model.query.filter_by(email=User).first()
        user.trackers.append(new_tracker)
        db.session.add(new_tracker)
        db.session.commit()
            
        str11 = "Tracker created."
        return jsonify(str11)

    @auth_required('token')
    def put(self,id,email):
        trackers = tracker.query.filter_by(id=id).first()
        args = tracker_post_args.parse_args()
        
        User = email
        Name=args.get("Tracker_name")
        Description=args.get('Tracker_Description',None)
        Tracker_type=args.get( 'Tracker_Type',None)
        Setting = args.get('Setting',None)
        if trackers:
            trackers.name = Name
            trackers.description = Description
            trackers.tracker_type = Tracker_type
            trackers.setting = Setting   
            db.session.commit()
            return jsonify("tracker updated.")
        return jsonify( {"error":"tracker id not valid"})

    @auth_required('token')
    def delete(self,id,email):
        new_tracker = tracker.query.filter_by(id=id).first()
        try: 
            db.session.delete(new_tracker)
            db.session.commit()
            return jsonify("Successfully Deleted.")
        except:
            return jsonify({"error":"id does not exist."})

# DateCreated = datetime.datetime.now(tz)
# format_date = DateCreated.strftime("%d/%m/%Y %H:%M:%S")

import base64
class LoggerAPI(Resource):
    @auth_required('token')
    def get(self,type,id):
        parent_tracker=tracker.query.filter_by(id=id).first()
        Name = parent_tracker.name
        Description =parent_tracker.description
        Tracker_type = parent_tracker.tracker_type
        Setting= parent_tracker.setting
        all_logs = parent_tracker.logs 

        log_ids = []
        for i in all_logs:
            # print(i.id)
            log_ids.append(i.id)
        details = []    
        for j in log_ids:    
            detail = logs.query.filter_by(id=j).first()
            details.append(detail)
            # print(detail.value)
        count = 0  
        d = {}  
        for k in details:
            count+=1
            track_dict = {"id":k.id ,"Value":k.value,"Note":k.note,"date_created": k.timestamp }
            d[count]=track_dict
        # return jsonify(d)
        # print(d)

        if type=="Numeric":
            data={x.timestamp:x.value 
            for x in all_logs}
            # print(data)
            plt.clf()
            plt.plot(data.keys(), data.values())
            plt.xlabel("Time Stamp")
            plt.ylabel("Value")
            plt.title("Numerical TrendLine")
            plt.savefig('./static/graph/graph_numeric.png')
            encoded = base64.b64encode(open("./static/graph/graph_numeric.png", "rb").read())
            new_encode = str(encoded)[2:-3]
            # plt.savefig('../client/src/assets/graph_numeric.png')
            plt.close()
            return jsonify(d,{"base64": str(new_encode),"base64_1": None,"base64_2": None})

        elif type=="Multiple Choice":
            data={x.timestamp:x.value 
            for x in all_logs}
            plt.clf()
            plt.plot(data.values(),data.keys(), marker='o',linestyle="dashed",linewidth=1)
            plt.ylabel("Time Stamp")
            plt.xlabel("Value")
            plt.title("Multiple Choice TrendLine")
            plt.savefig('./static/graph/graph_multiple.png')
            encoded = base64.b64encode(open("./static/graph/graph_multiple.png", "rb").read())
            new_encode1 = str(encoded)[2:-3]
            # plt.savefig('../client/src/assets/graph_multiple.png')
            plt.close()
            return jsonify(d,{"base64": None,"base64_1": str(new_encode1),"base64_2": None})
                  
        elif type=="Boolean":
            data={x.timestamp:x.value 
            for x in all_logs}
            plt.clf()
            plt.plot( data.values(),data.keys(),marker='o',linestyle="dashed",linewidth=1)
            plt.ylabel("Time Stamp")
            plt.xlabel("Value")
            plt.title("Boolean TrendLine")
            plt.savefig('./static/graph/graph_boolean.png')
            encoded = base64.b64encode(open("./static/graph/graph_boolean.png", "rb").read())
            new_encode2 = str(encoded)[2:-3]
            # plt.savefig('../client/src/assets/graph_boolean.png')
            plt.close()
            return jsonify(d,{"base64": None,"base64_1": None,"base64_2": str(new_encode2)})       
        return jsonify({"error":'Something Went SomeWhere. Out Type Don\'t Match'})

    @auth_required('token')
    def post(self,type,id):
        agrs = numeric_post_args.parse_args()
        args = multiple_post_args.parse_args()
        args1 = boolean_post_args.parse_args()

        parent_tracker=tracker.query.filter_by(id=id).first()

        Timestamp=logs.query.get("timestamp")
        if type == "Numeric":
            Value=agrs.get("Value")
            Note=agrs.get("Note")
            email = agrs.get("email")
            userr = user_model.query.filter_by(email=email).first()
            username = userr.username
            # print(Value)
            # data = str(Value) + str(Note) + str(type)
            if Value.isdigit(): 
                new_log=logs(log=type, value=Value, note=Note, timestamp=Timestamp)
                parent_tracker.logs.append(new_log)
                db.session.add(new_log)
                db.session.commit()
                job_id = task.daily_reminder.apply_async(args=[email,username],countdown=3000)
                str="Numeric Log Added Successfully"
                return jsonify(str)
            else:
                return jsonify( {"error" : "Invalid Value Provided"})
        elif type == "Multiple Choice":
            Setting=args.get("Value")
            Note=args.get("Note")
            email = agrs.get("email")
            userr = user_model.query.filter_by(email=email).first()
            username = userr.username
            # data = str(Setting) + str(Note) + str(type)
            set_ting = parent_tracker.setting
            # print(Setting)
            # print(Note)
            # [x.strip() for x in set_ting.split(',')]
            # list_setting = list(set_ting.split(",").strip())
            list_setting = [x.strip() for x in set_ting.split(',')]

            # print(list_setting)
            res1 = any(Setting == a for a in list_setting)
            # print(res1)
            if res1 == True:
                    new_log=logs(log=type, value=Setting, note=Note, timestamp=Timestamp)
                    parent_tracker.logs.append(new_log)
                    db.session.add(new_log)
                    db.session.commit()
                    job = task.daily_reminder.apply_async(args=[email,username],countdown=30)
                    str="Multiple Choice Log Added Successfully"
                    return jsonify(str)
            else:        
                return jsonify( {"error" : "Invalid Setting Provided"})
        # print(Name)
        elif type == "Boolean":
            Value=args1.get("Value")
            Note=args1.get('Note')
            email = agrs.get("email")
            userr = user_model.query.filter_by(email=email).first()
            username = userr.username
            # data = str(Value) + str(Note) + str(type)
            new_log=logs(log=type, value=Value, note=Note, timestamp=Timestamp)
            parent_tracker.logs.append(new_log)
            db.session.add(new_log)
            db.session.commit()
            job1 = task.daily_reminder.apply_async(args=[email,username],countdown=30)
            str="Boolean Log Added Successfully"
            return jsonify(str)
        return jsonify("Tracker id not valid.")
        
    @auth_required('token')
    def put(self,tracker_id,log_id):
        log_needed=logs.query.filter_by(id=log_id).first()
        trackers = tracker.query.filter_by(id=tracker_id).first()
        # args = tracker_post_args.parse_args()
        agrs = numeric_post_args.parse_args()
        args0 = multiple_post_args.parse_args()
        args1 = boolean_post_args.parse_args()
        # User = user
        if trackers.tracker_type == "Multiple Choice":
            Setting = args0.get('Value')
            Note = args0.get('Note')
            if log_needed:
                log_needed.value = Setting
                log_needed.note = Note
                db.session.commit()
                return jsonify("log multiple updated.")

        if trackers.tracker_type == "Numeric":
            Value = agrs.get('Value')
            Note = agrs.get('Note')
            if log_needed:
                log_needed.value = Value
                log_needed.note = Note
                db.session.commit()
                return jsonify("log numeric updated.")

        if trackers.tracker_type == "Boolean":
            Value = args1.get('Value')
            Note = args1.get('Note')
            if log_needed:
                log_needed.value = Value
                log_needed.note = Note
                db.session.commit()
                return jsonify("log Boolean updated.")    
        return jsonify( {"error":"tracker/log id not valid"})     

    @auth_required('token')
    def delete(self,tracker_id,log_id):
        log_needed = logs.query.get_or_404(log_id)
        new_tracker = tracker.query.get_or_404(tracker_id)
        try:
            if new_tracker and log_needed:
                db.session.delete(log_needed)
                db.session.commit()
                return jsonify("Deleted Successfully")
        except:        
            return jsonify({"error":"There was a problem deleting that task."})


log_fields = {
    'Value' : fields.Integer,
    'Note' : fields.String
}


class Export(Resource):
    @auth_required('token')
    def get(self,email):
        user = user_model.query.filter_by(email = email).first()
        username = user.username
        tracks  = user.trackers
        tracker_ids = []
        for i in tracks:
            # print(i.id)
            tracker_ids.append(i.id)
        details = []    
        for j in tracker_ids:    
            detail = tracker.query.filter_by(id=j).first()
            details.append(detail)
            # print(detail.name)
        count = 0  
        t = []
        # d = {}  
        for k in details:
            count+=1
            track_dict = {"id":count ,"Tracker_name":k.name,"Tracker_Description":k.description,"Tracker_Type":k.tracker_type, "Setting": k.setting , "date_created": str(k.date_created) }
            # d[count]=track_dict
            t.append(track_dict)
        # print(d," 3 ")
        # print(t, " 4 ")  
        job_id = task.export_csv.delay(t,email,username)    
        return f"Celery JoB strated for {job_id}",200


class Export_Log(Resource):
    @auth_required('token')
    def get(self,email,tracker_id):
        parent_tracker=tracker.query.filter_by(id=tracker_id).first()
        Name = parent_tracker.name
        Description =parent_tracker.description
        Tracker_type = parent_tracker.tracker_type
        Setting= parent_tracker.setting
        all_logs = parent_tracker.logs 
        user = user_model.query.filter_by(email = email).first()
        username = user.username

        log_ids = []
        for i in all_logs:
            # print(i.id)
            log_ids.append(i.id)
        details = []    
        for j in log_ids:    
            detail = logs.query.filter_by(id=j).first()
            details.append(detail)
            # print(detail.value)
        count = 0  
        t = []
        for k in details:
            count+=1
            track_dict = {"id":count ,"Value":k.value,"Note":k.note,"date_created": str(k.timestamp) }
            t.append(track_dict)
        # return jsonify(d)
        # print(d)
        if Tracker_type=="Numeric":
            data={x.timestamp:x.value 
            for x in all_logs}
            # print(data)
            plt.clf()
            plt.plot(data.keys(), data.values())
            plt.xlabel("Time Stamp")
            plt.ylabel("Value")
            plt.title("Numerical TrendLine")
            plt.savefig('./static/graph/graph_numeric.png')
            plt.close()      

        elif Tracker_type=="Multiple Choice":
            data={x.timestamp:x.value 
            for x in all_logs}
            plt.clf()
            plt.plot(data.values(),data.keys(), marker='o',linestyle="dashed",linewidth=1)
            plt.ylabel("Time Stamp")
            plt.xlabel("Value")
            plt.title("Multiple Choice TrendLine")
            plt.savefig('./static/graph/graph_multiple.png')  
            plt.close()

        elif Tracker_type=="Boolean":
            data={x.timestamp:x.value 
            for x in all_logs}
            plt.clf()
            plt.plot( data.values(),data.keys(),marker='o',linestyle="dashed",linewidth=1)
            plt.ylabel("Time Stamp")
            plt.xlabel("Value")
            plt.title("Boolean TrendLine")
            plt.savefig('./static/graph/graph_boolean.png')
            plt.close()

        job_id = task.export_csv_log.delay(t,email,Name,username,Description,Setting) 
        
        return f"we are done here {job_id}",200