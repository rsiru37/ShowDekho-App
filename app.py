from flask import Flask,render_template,request,redirect,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity,jwt_required,JWTManager
from flask_restful import Resource, Api,fields,marshal_with,reqparse,abort
from flask_cors import CORS
from celery.schedules import crontab
from celery.result import AsyncResult
from jinja2 import Environment, FileSystemLoader
import json
import pdfkit
import datetime
import time
import csv
import calendar
from celery_worker import make_celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask_caching import Cache

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']="yopies"
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cors=CORS(app)
jwt=JWTManager(app)
db=SQLAlchemy(app)
api=Api(app)
cache = Cache(app)
SMPTP_SERVER_HOST="DESKTOP-JHN6I7U"
SMPTP_SERVER_PORT=1025
SENDER_ADDRESS="email@shodekho.com"
SENDER_PASSWORD=""

class User(db.Model):
  id=db.Column(db.Integer, primary_key=True,autoincrement=True)
  name=db.Column(db.String(100), unique=True, nullable=False)
  email=db.Column(db.String(100), unique=True, nullable=False)
  pwd=db.Column(db.String(100), nullable=False)
  admin=db.Column(db.Boolean)
  last_loggedin=db.Column(db.DateTime)
  theatres=db.relationship('Theatre',cascade='all,delete', backref='admin')
  movies=db.relationship('Movie', cascade='all,delete', backref='admin')
  shows=db.relationship('Show', cascade='all,delete', backref='admin')
  bookings=db.relationship('Booking', backref='user',lazy=True)

class Movie(db.Model):
  mid=db.Column(db.Integer, primary_key=True,autoincrement=True)
  mname=db.Column(db.String(100), unique=True, nullable=False)
  director=db.Column(db.String(100))
  duration=db.Column(db.Integer)
  summary=db.Column(db.String)
  ratings=db.Column(db.Float, nullable=False)
  shows=db.relationship('Show', cascade='all,delete', backref='movie',lazy=True)
  madmin=db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')) # The Person who creates the Movie(Admin)

class Theatre(db.Model):
  tid=db.Column(db.Integer, primary_key=True,autoincrement=True)
  tname=db.Column(db.String(100), unique=True, nullable=False)
  city=db.Column(db.String(50), nullable=False)
  pincode=db.Column(db.Integer, nullable=False)
  capacity=db.Column(db.Integer,nullable=False)
  contact=db.Column(db.Integer, unique=True)
  tadmin=db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')) # The person who created the Theatre
  shows=db.relationship('Show', backref='theatre',cascade='all, delete-orphan', lazy='select')

class Show(db.Model):
  sid=db.Column(db.Integer, primary_key=True,autoincrement=True)
  ticket_price=db.Column(db.Integer, nullable=False)
  stime=db.Column(db.DateTime, nullable=False)
  moid=db.Column(db.Integer(), db.ForeignKey('movie.mid', ondelete='CASCADE')) # To which Movie is this Movie Associated to
  thid=db.Column(db.Integer,db.ForeignKey('theatre.tid', ondelete='CASCADE')) # To which theatre is this movie Associated to
  sadmin=db.Column(db.Integer,db.ForeignKey('user.id', ondelete='CASCADE')) # The person who creates the Show(Admin)
  available_seats=db.Column(db.Integer(), nullable=False)
  bookings=db.relationship('Booking', backref='show', lazy=True)


class Booking(db.Model):
  bid=db.Column(db.Integer, primary_key=True,autoincrement=True)
  uid=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
  shid=db.Column(db.Integer, db.ForeignKey('show.sid'))
  seats=db.Column(db.Integer)
  booking_date=db.Column(db.DateTime,nullable=False)
  movie_name=db.Column(db.String(100))
  tid=db.Column(db.String(100))
  theatre_name=db.Column(db.String(100))
  show_time=db.Column(db.DateTime)
  ticket_price=db.Column(db.Integer)


######### CELERY ##########
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1'
    #CELERY_RESULT_BACKEND='redis://localhost:6379/1'
)
celery = make_celery(app)

@celery.task() # Define all the Async Functions in this format...
def create_pdf():
  users=User.query.filter_by(admin=0).all() # Listing all the Users
  for user in users:
    temp_html= gen_html(user)
    pdfkit.from_string(temp_html,f'{user.id}.pdf')
    send_pdf_mail.delay(user.email, f'Monthly Report from ShowDekho', f'Hi {user.name}, Please find below your attached Montly Bookings Report', user.id)

@celery.task
def send_pdf_mail(to,sub,body,id):
  msg=MIMEMultipart()
  msg["From"]=SENDER_ADDRESS
  msg["To"]=to
  msg["Subject"]=sub
  msg.attach(MIMEText(body,'plain'))
  with open(f'./{id}.pdf', "rb") as file:
    part = MIMEApplication(file.read(), Name=f'{id}.pdf')
    part['Content-Disposition'] = f'attachment; filename="{part["Name"]}"'
    msg.attach(part)
    s=smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery.task()
def gen_html(user):
  total_cost=0
  env = Environment(loader=FileSystemLoader('.'))
  final_booking_data=[]
  now=datetime.datetime.now()
  #Now we are fetching all the bookings for a particular user from 1st of the month till the date when we are generating this report
  bookings=Booking.query.filter(Booking.booking_date<now, Booking.booking_date>datetime.datetime(now.year, now.month-1,1,0,0,0), Booking.uid==user.id).all()
  #bookings=user.bookings
  name=user.name
  if(datetime.datetime.now().month ==1):
      month='December'
  else:
      month=calendar.month_name[datetime.datetime.now().month -1] # Since we will trigger the Task on 1st of Every month, When January Comes we need report for December
  for book in bookings:
    booking_data={}
    booking_data['id']=book.bid
    booking_data['seats']=book.seats
    booking_data['booking_date']=f'{book.booking_date.day} / {book.booking_date.month} / {book.booking_date.year}'
    booking_data['booking_time']=f'{book.booking_date.hour} : {book.booking_date.minute}'
    booking_data['show_date']=f'{book.show_time.day} / {book.show_time.month} / {book.show_time.year}'
    booking_data['show_time']=f'{book.show_time.hour} : {book.show_time.minute}'
    booking_data['total_cost']=book.seats*book.ticket_price
    total_cost+=booking_data['total_cost']
    booking_data['movie']=book.movie_name
    booking_data['theatre']=book.theatre_name
    final_booking_data.append(booking_data)
  template=env.get_template('user_report.html')
  return template.render(final_booking_data=final_booking_data,total_cost=total_cost,name=name,month=month)

@celery.task()
def gencsv(id):
  theatre=Theatre.query.filter_by(tid=id).first()
  # shows=theatre.shows
  # movi=set()
  # for show in shows:
  #   movi.add(show.movie.mid)
  # movi=list(movi)
  # movies=[Movie.query.filter_by(mid=x).first() for x in movi]
  # data_rows = [['This', "Report", "is", "For" ,theatre.tname, theatre.city, 'Capacity','Of', theatre.capacity],[]]
  # data_rows.append(['List','Of','Movies', 'Hosted', ':']+[movie.mname for movie in movies])
  # data_rows.append([])
  # data_rows.append(['MOVIE NAME', 'SHOWTIME', 'SEATS BOOKED', 'REVENUE GENERATED'])
  # for movie in movies:
  #   for show in movie.shows:
  #     data_rows.append([movie.mname, show.stime, sum(book.seats for book in show.bookings), sum(book.seats for book in show.bookings)*show.ticket_price])
  bookings=Booking.query.filter_by(tid=id).all()
  data_rows = [['This', "Report", "is", "For" ,theatre.tname, theatre.city, 'Capacity','Of', theatre.capacity],[],[]]
  data_rows.append(['MOVIE NAME', 'SHOWTIME', 'SEATS BOOKED', 'REVENUE GENERATED'])
  for book in bookings:
    data_rows.append([book.movie_name, book.show_time, book.seats, book.ticket_price*book.seats])
  with open(f'admin_report_{theatre.tid}.csv', mode='w', newline='') as file:
    writer=csv.writer(file)
    writer.writerows(data_rows)
  return f'admin_report_{theatre.tid}.csv'

@celery.task()
def send_email(to,subject,mesg):
  msg=MIMEMultipart()
  msg["From"]=SENDER_ADDRESS
  msg["To"]=to
  msg["Subject"]=subject

  msg.attach(MIMEText(mesg,'html'))
  s=smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
  s.login(SENDER_ADDRESS,SENDER_PASSWORD)
  s.send_message(msg)
  s.quit()
  return True

@celery.task
def send_daily_mail():
  users=User.query.filter_by(admin=0).all() # Filtering all the Users
  time_now=datetime.datetime.now()
  start_day=datetime.datetime(time_now.year,time_now.month,time_now.day,6,0,0)
  for user in users:
    if(user.last_loggedin):
      if(not(start_day<=user.last_loggedin and user.last_loggedin<=time_now)):
        send_email(user.email,"Feeling Bored!? Wanna Watch a Movie? Book Right Now ", f"Hi {user.name}, Hope you are Doing fine, we Noticed You havent booked any of the Movie tickets on our App ShowDekho.com, We have uploaded the Latest collection of Movies and Hoping you could have a look, Do Check them out before the Tickets are out! Have a Good Day Ahed")
    else:
      send_email(user.email,"Feeling Bored!? Wanna Watch a Movie? Book Right Now ", f"Hi {user.name}, Hope you are Doing fine, we Noticed You havent booked any of the Movie tickets on our App ShowDekho.com, We have uploaded the Latest collection of Movies and Hoping you could have a look, Do Check them out before the Tickets are out! Have a Good Day Ahed")      
  return 'Mail Sent! Check ur Inbox'


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17,minute=37),send_daily_mail.s(), name="Daily Reminder Task")
    sender.add_periodic_task(crontab(0, 0, day_of_month='1'),create_pdf.s(), name="Monthly Maintenence Report")



@app.route('/download-file/<string:path>')
def download_file(path):
  return send_file(path)
############################################################################################################################################################################

class Piture(Resource):
  @cache.cached(timeout=10, key_prefix='movies')
  def get(self):
    t={}
    limo=[]
    x=Movie.query.all()
    for m in x:
      t['id']=m.mid       
      t['name']=m.mname
      t['director']=m.director
      t['duration']=m.duration
      t['summary']=m.summary
      t['ratings']=m.ratings
      limo.append(t)
      t={}
    return jsonify(limo) 
  

class Logo(Resource):
  def post(self): # Login
    email=request.get_json()['email']
    pwd=request.get_json()['pwd']
    admin=request.get_json()['admin']
    a=User.query.filter_by(email=email, pwd=pwd).first()
    if(a):
      access_token = create_access_token(identity=a.id, expires_delta=datetime.timedelta(hours=1))
      a.last_loggedin=datetime.datetime.now()
      db.session.commit()
      if(a.admin and admin):
        d={'at':access_token, 'msg':"Login Successful", 'admin':a.name}
        return jsonify(d)
      else:
        d={'at':access_token, 'msg':"Login Successful", 'user':a.name}
        return jsonify(d)
    else:
      return jsonify('Login Failed')
    
class UserAuth(Resource):
  @jwt_required()
  def get(self):
    c_id=get_jwt_identity()
    user=User.query.get(c_id)
    return jsonify(user.name)
  ############################################## MOVIES #######################################################
class Movid(Resource):
  def get(self):
    movie=Movie.query.filter_by(mid=request.args.get('movie_id')).first()
    return jsonify(
      {'director':movie.director, 'duration':movie.duration,'ratings':movie.ratings,'summary':movie.summary})    

  @jwt_required()
  def post(self):
    movie_name=request.get_json()['movie_name']
    movie_director=request.get_json()['movie_director']
    movie_duration=request.get_json()['movie_duration']
    movie_ratings=request.get_json()['movie_ratings']
    movie_summary=request.get_json()['movie_summary']
    admin=request.get_json()['admin_name']
    movie=Movie.query.filter_by(mname=movie_name).first() # We are checking if any movie exists with the Same Name?
    try:
      admin=User.query.filter_by(name=admin).first()
      if(admin.admin and not(movie)):
        m=Movie(mname=movie_name,director=movie_director,duration=movie_duration,summary=movie_summary,ratings=movie_ratings)
        admin.movies.append(m)
        db.session.commit()
        return jsonify("Movie Creation Successful!")
      else:
        return jsonify("Movie with Same name already exists, Try with a Different Name")
    except Exception as e:
      return jsonify(str(e))
  
  @jwt_required()
  def put(self):
    movie_name=request.get_json()['movie_name']
    movie_director=request.get_json()['movie_director']
    movie_duration=request.get_json()['movie_duration']
    movie_ratings=request.get_json()['movie_ratings']
    movie_summary=request.get_json()['movie_summary']
    mid=request.get_json()['movie_id']
    movie=Movie.query.filter_by(mname=movie_name).first() # We are checking if any movie exists with the Same Name?
    if(movie):
      return "Movie with Same name already exists, Try with a Different Name"
    try:
      movie=Movie.query.filter_by(mid=mid).first()
      movie.mname=movie_name
      movie.director=movie_director
      movie.duration=movie_duration
      movie.ratings=movie_ratings
      movie.summary=movie_summary
      db.session.commit()
      return jsonify('Update Successfull')
    except Exception as e:
      return jsonify(str(e))
    
  @jwt_required()
  def delete(self):
    movie_id=request.get_json()['movie_id']
    try:
      movie=Movie.query.filter_by(mid=movie_id).first()
      db.session.delete(movie)
      db.session.commit()
      return jsonify('Delete Sucessful')
    except Exception as e:
      return jsonify(str(e))
##############################################################################################################################

########################################################THEATRES#########################################################

class Theatres(Resource):
  @cache.cached(timeout=10, key_prefix='theatres')
  @jwt_required()
  def get(self):
    theatre_dict={}
    theatre_list=[]
    for theatre in Theatre.query.all():
      theatre_dict['tid']=theatre.tid
      theatre_dict['tname']=theatre.tname
      theatre_dict['city']=theatre.city
      theatre_dict['pincode']=theatre.pincode
      theatre_dict['capacity']=theatre.capacity
      theatre_dict['contact']=theatre.contact
      theatre_list.append(theatre_dict)
      theatre_dict={}
    return jsonify(theatre_list)
  
  @jwt_required()
  def post(self):
    params=request.get_json()
    aid=get_jwt_identity()
    if(Theatre.query.filter_by(tname=params['tname']).first()):
      return 'Theatre with the Same name already exists, Try with a Different Name'
    theatre=Theatre(tname=params['tname'], city=params['city'], pincode=params['pincode'], capacity=params['capacity'], contact=params['contact'], tadmin=aid)
    db.session.add(theatre)
    db.session.commit()
    return 'Theatre Added Successfully!'
  
  @jwt_required()
  def put(self):
    params=request.get_json()['data']
    if(Theatre.query.filter_by(tname=params['theatre_name']).first()):
      return jsonify('Theatre with Same name already Exists, Try with a Different Name')
    theatre=Theatre.query.filter_by(tid=params['theatre_id']).first()
    theatre.tname=params["theatre_name"]
    theatre.city=params['theatre_city']
    theatre.pincode=params['theatre_pincode']
    theatre.contact=params['theatre_contact']
    theatre.capacity=params['theatre_capacity']
    db.session().commit()
    return jsonify('Update Successfull!!')

  @jwt_required()
  def delete(self):
    theatre=Theatre.query.filter_by(tid=request.get_json()['theatre_id']).first()
    db.session.delete(theatre)
    db.session.commit()
    return 'Deleted Successfully!'

class ShowTheatre(Resource):
  @jwt_required()
  def get(self,id):
    sd={}
    show=Show.query.filter_by(sid=id).first()
    sd['ticket_price']=show.ticket_price
    sd['date_time']=show.stime
    sd['available_seats']=show.available_seats
    sd['total_seats']=show.theatre.capacity
    sd['movie_id']=show.moid
    sd['theatre_id']=show.thid
    return jsonify(sd)


class Shows(Resource):
  @jwt_required()
  def get(self,id):
    movie=Movie.query.filter_by(mid=id).first()
    shows=movie.shows
    show_dict={}
    shows_list=[]
    for show in shows:
      show_dict['price']=show.ticket_price
      show_dict['month']=show.stime.month
      show_dict['date']=show.stime.day
      show_dict['hour']=show.stime.hour
      show_dict['minute']=show.stime.minute
      show_dict['hour']='00' if show.stime.hour==0 else show_dict['hour']
      show_dict['minute']='00' if show.stime.minute==0 else show_dict['minute']
      show_dict['theatre_name']=show.theatre.tname
      show_dict['available_seats']=show.available_seats
      show_dict['id']=show.sid
      show_dict['movie_name']=movie.mname
      show_dict['city']=show.theatre.city
      show_dict['pincode']=show.theatre.pincode
      shows_list.append(show_dict)
      show_dict={}
    return jsonify(shows_list)



class Showsapi(Resource):
  #@cache.cached(timeout=120, key_prefix='shows')
  @jwt_required()
  def get(self):
    sd={}
    sl=[]
    shows=Show.query.all()
    for s in shows:
      sd['id']=s.sid
      sd['price']=s.ticket_price
      sd['month']=s.stime.month
      sd['date']=s.stime.day
      sd['hour']=s.stime.hour
      sd['minute']=s.stime.minute
      sd['year']=s.stime.year
      sd['hour']='00' if s.stime.hour==0 else sd['hour']
      sd['minute']='00' if s.stime.minute==0 else sd['minute']
      sd['movie']=s.movie.mname
      sd['theatre']=s.theatre.tname
      sd['available_seats']=s.available_seats
      sl.append(sd)
      sd={}
    return jsonify(sl)
  
  @jwt_required()
  def post(self):
    params=request.get_json()
    mid=params['a']
    tid=params['b']
    dt=params['c'].split('-')
    ticket_price=params['d']
    year=int(dt[0])
    month=int(dt[1])
    day=int(dt[2][0:2])
    hour=int(dt[2][3:5])
    minute=int(dt[2][6:])
    show=Show(ticket_price=ticket_price,stime=datetime.datetime(year,month,day,hour,minute),moid=mid,thid=tid,available_seats=Theatre.query.filter_by(tid=tid).first().capacity, sadmin=get_jwt_identity())
    db.session.add(show)
    db.session.commit()
    return 'Show Added Successfully!'

  @jwt_required()
  def put(self):
    params=request.get_json()
    mid=params['a']
    tid=params['b']
    dt=params['c'].split('-')
    ticket_price=params['d']
    sid=params['e']
    year=int(dt[0])
    month=int(dt[1])
    day=int(dt[2][0:2])
    hour=int(dt[2][3:5])
    minute=int(dt[2][6:])
    show=Show.query.filter_by(sid=sid).first()
    show.moid=mid
    show.thid=tid
    show.ticket_price=ticket_price
    show.stime=datetime.datetime(year,month,day,hour,minute)
    db.session.commit()
    return 'Updated Sucessfully!'

  @jwt_required()
  def delete(self):
    db.session.delete(Show.query.filter_by(sid=request.get_json()['show_id']).first())
    db.session.commit()
    return 'Deleted Successfully!'


class Thid(Resource):
  def get(self,id):
    theatre=Theatre.query.filter_by(tid=id).first()
    return jsonify({'tname':theatre.tname, 'city':theatre.city, 'pincode':theatre.pincode, 'capacity':theatre.capacity, 'contact':theatre.contact, 'tid':theatre.tid})

class Book(Resource):
  @jwt_required()
  def post(self):
    uid=get_jwt_identity()
    params=request.get_json()['dd']
    show=Show.query.filter_by(sid=params['show_id']).first()
    show.available_seats=show.available_seats-int(params['seats'])
    book=Booking(uid=uid,shid=params['show_id'],seats=int(params['seats']), booking_date=datetime.datetime.now(),movie_name=show.movie.mname,tid=show.theatre.tid,theatre_name=show.theatre.tname,show_time=show.stime,ticket_price=show.ticket_price)
    db.session.add(book)
    db.session.commit()
    return 'Booking Success!'

class Report(Resource):
  @jwt_required()
  def get(self,id):
    k=gencsv.delay(id)
    while(not(k.ready())):
      print('H', k.ready())
    return k.result

class Signup(Resource):
  def post(self):
    email=request.get_json()['email']
    pwd=request.get_json()['pwd']
    name=request.get_json()['name']
    n_user=User.query.filter_by(name=name).first()
    e_user=User.query.filter_by(email=email).first()
    if(n_user or e_user):
      return 'Username/Email Already exists try with a different name/email'
    user=User(name=name,email=email,pwd=pwd,admin=0)
    db.session.add(user)
    db.session.commit()
    return 'User Created Successfully!'

api.add_resource(Logo,'/logi') #USER LOGIN
api.add_resource(Piture,'/home') # DISPLAY OF MOVIES AT HOMEPAGE OF USER/ADMIN(GET ONLY)
api.add_resource(UserAuth,'/uauth')
api.add_resource(Movid,'/movie') #ADMIN (CUD) OF MOVIES & Getting Movie Info for a movie id
api.add_resource(Shows,'/shows/<int:id>') # Getting SHOWS FOR A MOVIE(USER ONLY)
api.add_resource(Theatres,'/theatre') #THEATRE CRUD
api.add_resource(Thid,'/theatre/<int:id>')#Getting a THEATRES INFO BY THEATRE_ID
api.add_resource(Showsapi,'/shows') # Getting All the Shows INFO
api.add_resource(ShowTheatre,'/show/<int:id>') # Admin editing a Show
api.add_resource(Book,'/booking') # USER BOOKING TICKETS
api.add_resource(Report,'/report/<int:id>')
api.add_resource(Signup,'/usersignup') # USER SIGNUP

if __name__=='__main__':
  app.run(debug=True)