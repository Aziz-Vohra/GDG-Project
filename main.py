import requests
import bs4
base_link = 'https://summerofcode.withgoogle.com'
organisations_links = []
org_links = []
org_tech = []
org_name = []
org_descp = []
org_topics = []
org_mail = []
res = requests.get('https://summerofcode.withgoogle.com/archive/2017/organizations/'
                   )
soup = bs4.BeautifulSoup(res.content,"lxml")
links = soup.find_all("a",{'class':"organization-card__link"})
for link in links:
    organisations_links.append(base_link + link.get('href'))
    for org in organisations_links:
    res1 = requests.get(org)
    soup1 = bs4.BeautifulSoup(res1.content,"lxml")
    org_links.append(soup1.find("a",{'class':"org__link"}).get('href'))
    techn =  soup1.find_all("li" ,{'class':'organization__tag organization__tag--technology'})
    tl = []
    for tech in techn:
        tl . append(tech.string)
    org_tech.append(tech)
    meta_button = soup1.find_all("md-button",{"class":"md-primary org__meta-button"})
    org_mail.append(meta_button[-1].get('href')[7:])
    decp = soup1.find('div',{'class':"archive-project-card__content md-padding font-black-54" })
    if decp is None:
        org_descp.append("none")
    else:
        org_descp.append(decp.string)
    org_name.append( soup1.find('h3',{ 'class':"banner__title"}).string)
    print("success")
print("success final")
import sqlite3

conn = sqlite3.connect('GSOC_ORG.db')
print("Opened database successfully");

conn.execute('''CREATE TABLE ORGS
         (
         organization   TEXT    NOT NULL,
         link            TEXT,
         description    TEXT,
         technologies   TEXT,
         contact    TEXT
         );''')
print("Table created successfully");
for i in range(len(organisations_links)):
    conn.execute("INSERT INTO ORGS VALUES('"+org_name[i]+ "','"+str(org_links[i])+"','"+str(org_descp[i])+"','"+str(org_tech[i])+"','"+str(org_mail[i])+"');")
print("successfull database")
conn.close()
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

db_connect = create_engine('sqlite:////' +'Users/shreyashkawalkar/Developer/GDG Project/GDG-Project/GSOC_ORG.db')
app = Flask(__name__)
api = Api(app)

class Organisations(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from ORGS") # This line performs query and returns json result
        
        for i in query.cursor.fetchall():
            print(i)
        return {'Organisations': [i[0] for i in query.cursor.fetchall()]}

api.add_resource(Organisations, '/organisations') # Route_1


if __name__ == '__main__':
     app.run(port='5002')
    from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'GSOC_ORG.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organisation = db.Column(db.TEXT, unique=True)
    link = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    technologies = db.Column(db.TEXT)
    contact = db.Column(db.TEXT)
    def __init__(self, organisation, link, description, technologies, contact):
        self.organisation = organisation
        self.link = link
        self.description = description
        self.technologies = technologies
        self.contact = contact
        


class orgs(ma.Schema):
    class Meta:
        fields = ('organisation', 'link', 'description', 'technologies', 'contact')

orgs_schema = orgs(many=True)


@app.route("/organisations", methods=["GET"])
def get_orgs():
    all_orgs = org.query.all()
    result = orgs_schema.dump(all_orgs)
    return jsonify(result.data)


if __name__ == '__main__':
    app.run(debug=True)
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(0)
