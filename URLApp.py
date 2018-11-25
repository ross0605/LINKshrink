from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker, load_only
from tabledef import *
from flask_recaptcha import ReCaptcha
from random import choice
import string
import validators
import requests
import json
from flask_bcrypt import (Bcrypt, check_password_hash, generate_password_hash)

engine = create_engine('sqlite:///database.db', echo=True)

app = Flask(__name__)
app.secret_key = os.urandom(12)
bcrypt = Bcrypt(app)


app.config.update({'RECAPTCHA_ENABLED': True, 'RECAPTCHA_SITE_KEY':'6LcEunkUAAAAAFHhAGgUWR2gFXdKlV7wk0AktVO0', 'RECAPTCHA_SECRET_KEY':'123456789secretkey'})

recaptcha=ReCaptcha(app=app)


@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('homepageNOLOG.html')
	else:
		return render_template('homepageLOG.html')



@app.route('/loginpage')
def login():
	if not session.get('logged_in'):
		return render_template('loginpage.html')
	else:
		return "Logged in! <a href='/logout'>Logout</a>"



@app.route('/signuppage')
def signup():
	if not session.get('logged_in'):
		return render_template('signuppage.html')
	else:
		return render_template('homepageLOG.html')




@app.route('/loginToApp', methods=['POST'])
def do_admin_login():

	error = None
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]))
	result = query.first()
	if result:
		queryPass = s.query(User).filter_by(username=request.form['username'])
		for row in queryPass:
			passW = row.password
			if bcrypt.check_password_hash(passW, POST_PASSWORD):
				session['logged_in'] = True
				return redirect ("/")
			else:
				error = "Incorrect Password."
				return render_template('loginpage.html', error=error)
	else:
		error = "Username not recognised."
		return render_template('loginpage.html', error=error)


@app.route('/signupToApp', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		
		error = None
	
		new_user = User(name=request.form['name'], username=request.form['username'], password=(bcrypt.generate_password_hash(request.form['password'])))
		
		Session = sessionmaker(bind=engine)
		s = Session()

		exists = s.query(User.id).filter_by(username=request.form['username']).scalar()
		
		
                if exists is not None:
                        error = 'username already exists.'
        	        return render_template('signuppage.html', error=error)
	

		else:

			s.add(new_user)
			s.commit()


			query = s.query(User).order_by(User.id)
        		for _row in query.all():
                		print(_row.id, _row.name, _row.username, _row.password)
				
			return redirect ("/")	
			

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()



@app.route('/shorten', methods=['GET', 'POST'])
def shorten():
	def gen():
		chars = string.ascii_letters + string.digits
		length = 4
		code = ''.join(choice(chars) for x in range(length))
		return code
				
	code = gen()
	while code is None:
		code = gen()
	
	if request.method == 'POST':
			
		if validators.url(request.form['urllong']):

			if not session.get('logged_in'):
		
				r = requests.post('https://www.google.com/recaptcha/api/siteverify',
				   data = {'secret' :
				   '6LcEunkUAAAAAJEeacC-Uf6HK1ySATpcQLpJE3ot',
				   'response' :
				   request.form['g-recaptcha-response']})
	 
     			 	google_response = json.loads(r.text)	  
 				print('JSON: ', google_response)
       		 		
				if google_response['success']:			
		
					url = None
		
					Session = sessionmaker(bind=engine)
					s = Session()
		
					exists = s.query(URLTab.id).filter_by(urllong=request.form['urllong']).scalar()
					if exists is not None:
						query = s.query(URLTab.urlshort).filter_by(urllong=request.form['urllong'])
                                 	        for row in query:
							url = row.urlshort
                                                       	oldurl = request.form['urllong']
                                                       	return render_template('homepageNOLOG.html', url=url, oldurl=oldurl)
                                       	else:
                                               	short = 'set09103.napier.ac.uk:9147/'
                                               	new_url = URLTab(request.form['urllong'], urlshort= short + code)
                                               	s.add(new_url)
						s.commit()

                                   	        url = new_url.urlshort
                                      	        oldurl = request.form['urllong']

                                               	return render_template('homepageNOLOG.html', url=url, oldurl=oldurl)

			
				else:
					valid = "Captcha not valid"
					return render_template('homepageNOLOG.html', valid=valid)


			else:
				
				url = None

				Session = sessionmaker(bind=engine)
				s = Session()

				exists = s.query(URLTab.id).filter_by(urllong=request.form['urllong']).scalar()
				if exists is not None:
					query = s.query(URLTab.urlshort).filter_by(urllong=request.form['urllong'])
					for row in query:
						url = row.urlshort
						oldurl = request.form['urllong']
						return render_template('homepageNOLOG.html', url=url, oldurl=oldurl)
				else:
					short = 'set09103.napier.ac.uk:9147/'
					new_url = URLTab(request.form['urllong'], urlshort= short + code)
					s.add(new_url)
					s.commit()
	
					url = new_url.urlshort
					oldurl = request.form['urllong']
	
					return render_template('homepageNOLOG.html', url=url, oldurl=oldurl)
	
		else:
			valid = "Please enter a valid URL."
			return render_template('homepageNOLOG.html', valid=valid)
	
	
	
@app.route("/<url>")
def directto(url):

	shortaddress = url
	fullshort = "set09103.napier.ac.uk:9147/" + url
	
	Session = sessionmaker(bind=engine)
	session = Session()
	
	print shortaddress
	print (fullshort)

	exists = session.query(URLTab.id).filter_by(urlshort=fullshort).scalar()
	if exists is not None:
		query = session.query(URLTab.urllong).filter_by(urlshort=fullshort)
		for row in query:
			url = row.urllong
			return redirect (url)
	else:
		valid = "Short URL not recognised. Please shorten your link again or check that your short link is correct."
		return render_template('homepageNOLOG.html', valid=valid)



if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
