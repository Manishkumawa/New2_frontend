from flask import Flask,request,jsonify,redirect ,session ,url_for
from flask_jwt_extended import JWTManager,jwt_required,create_access_token ,get_jwt_identity
from pymongo import MongoClient

from gridfs import GridFS
from flask_cors import CORS
import os

#from authlib.integrations.flask_client import OAuth
import datetime 
app  = Flask(__name__)
CORS(app, origins='http://localhost:5173', supports_credentials=True)

app.secret_key = os.urandom(12)
#oauth = OAuth(app)

app.config['JWT_SECRET_KEY'] ='manish'
jwt = JWTManager(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['AI_database']

#google authenications system 
'''
@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = 'YOUR GOOGLE CLIENT ID'
    GOOGLE_CLIENT_SECRET = 'YOUR GOOGLE CLIENT SECRET'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect('/')

    '''

@app.route('/chef/signup' ,methods =['POST'])
def sign_up():

    if request.method  == 'POST':
        data = request.get_json()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        password_repeat= data.get('password_repeat')
        


        exist_user  =db.AllUser.find_one({'email':email},{'first_name':1})
        print(first_name)

        if exist_user:
            return jsonify({"message":"User Already registered"}),409
        if password != password_repeat:
            return jsonify({'Message':'Password not match'})
        db.AllUser.insert_one({'first_name':first_name ,'last_name':last_name,'email':email,'password':password})
        
        return jsonify({'message':'SignUp Successful'}),201
  
@app.route('/chef/login' ,methods =['POST'])
def login():
    if request.method =='POST':
        data=request.get_json()

        email = data.get('email')
        password  = data.get('password')

        login_user = db.AllUser.find_one({'email':email ,'password':password})
        if login_user:
            access_token = create_access_token(identity= email)

            return jsonify(message = 'Login Successful',access_token = access_token)
        else:
            return  jsonify({'Message':'Invalid email and password'}),401

           

@app.route('/chef/createDish',methods = ['POST'])
@jwt_required()
def create_dish():
    
    user_info = get_jwt_identity()
    first_name = user_info['first_name']
    last_name  = user_info['last_name']
    name = first_name  +last_name

    dish_name =  request.form["name"]
    veg_non_veg = request.form["veg_non_veg"]
    description = request.form["description"]

    pop_state = request.form["popularity_state"]

    cuisine = request.form["cuisine"]
    kitchen_equi = request.form["kitchen_equipments"]
    course_type = request.form["course_type"]

    ingredients = request.get_json()
    instructions = request.get_json()







    formatted_time = datetime.datetime.now().strftime("%H:%M:%S")
    formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    db.Dish.insert_one({'dish_name':dish_name ,'veg_Non':veg_non_veg ,'description':description ,"Popularity_state":pop_state ,"created_by":name ,"Cuisine":cuisine,"kitchen_equi":kitchen_equi,"course_type":course_type,"created_date":formatted_date,"created_time":formatted_time ,"quantity":quantity,"unit":unit,"i_name":i_name})
    
    return jsonify({'Message':'Dished Saved Successfully'}),201
    


@app.route('/nextPage',methods = ['GET'])
@jwt_required()
def nextPage():

    user_info = get_jwt_identity()   
   
    first_name = user_info['first_name']
    last_name  = user_info['last_name']
    name = first_name +last_name

    dis = db.Dish.find({"created_by":name})
    '''
    output =[]

    for dish in dis:
        dish_data = {
            "dish_name" :dish['dish_name'],
            "cuisine":dish['cuisine'],
            "veg_non":dish['veg_non'],
            "course_type":dish['course_type'],
            "created_date":dish['created_date'],
            "created_time":dish['created_time'],
            "description":dish['Description']   
        }
        output.append(dish_data)

        '''
    
        

    return jsonify({'list_of_dishes':dis,"user":name})



@app.route('/api/contact',methods =['POST'])
def contact():

    data = request.get_json()
    name = data['name']
    email = data['email']
    message =data['message']

    db.Contact.insert_one({'name':name,'email':email ,'message':message})

    return jsonify({"Message":"Message submitted succesfully"})

if __name__ =="__main__":
    app.run(debug= True)
    