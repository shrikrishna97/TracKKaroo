from workers import celery
from jinja2 import Template
from weasyprint import HTML
from mela import send_email
import csv


@celery.task()
def daily_reminder(email,username):
    with open('./templates/daily_reminder.html','r') as f:
        template = Template(f.read())
    send_email(email,'Daily Reminder',template.render(user=username),content="html")
    return "Daily reminder sent"

def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)


def pdf_report(d,User):
    msg = format_report("./templates/report.html",data=d,User=User)
    # print(msg)
    html = HTML(string=msg)
    # print(html)
    file_name = str(User)+"_tracK_Karoo"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)   


@celery.task()
def export_csv(d,email,username):
    with open('./static/tracker_info.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=d[0].keys(),restval='')
        file.writeheader()
        file.writerows(d)
    
    # pdf_report(d,username)

    with open('./templates/csv_tracker.html','r') as f:
        template = Template(f.read())
    send_email(email,'Exported Tracker Details',template.render(user=username,data=d),content="html",attachment="./static/tracker_info.csv")    
    return "Csv created." 



@celery.task()
def export_csv_log(d,email,Name,username,description,setting="No Settings"):
    with open('./static/logger_info.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=d[0].keys(),restval='')
        file.writeheader()
        file.writerows(d)
    
    with open('./templates/csv_log.html','r') as f:
        template = Template(f.read())
    send_email(email,'Exported Log Details',template.render(user=username,Name=Name,data=d,setting=setting,description=description),content="html",attachment="./static/logger_info.csv")    
    return "Csv created for log." 