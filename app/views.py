"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""
import os
from app import app
from app import db
from datetime import *
from app.models import User
from flask import render_template, request, redirect, url_for,jsonify,Response
from app.forms import ProfileForm
from werkzeug import secure_filename
import json
import time

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif','png'])

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profile',methods=['GET','POST'])
def profile():
    form = ProfileForm(request.form)
    if request.method == 'POST':
        uploadedfile = request.files['uploadedfile']
        if uploadedfile and allowed_file(uploadedfile.filename):
            uploadedfilename = form.username.data + '_' + secure_filename(uploadedfile.filename)
            filepath = os.path.join(os.getcwd() + '/app/static/uploads/',uploadedfilename)
            uploadedfile.save(filepath)
        user = User(uploadedfilename,form.username.data,form.firstname.data,form.lastname.data,form.biography.data,form.age.data,form.sex.data,datetime.now())
        db.session.add(user)
        db.session.commit()
        return redirect('/profile/'+str(User.query.filter_by(username=user.username).first().id))
    else:
        return render_template('profileform.html',form=form)
        
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/profile/<userid>', methods=['POST', 'GET'])
def selectedprofile(userid):
  user = User.query.filter_by(id=userid).first()
  image = '/static/uploads/' + user.userimage
  if request.method == 'POST' or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
    return jsonify(id=user.id, image=image,username=user.username, sex=user.usersex, age=user.userage, biography=user.biograpy,addedon=user.useraddon)
  else:
    user = {'id':user.id,'image':image, 'username':user.username,'fname':user.userfname, 'lname':user.userlname,'biography':user.biography,'age':user.userage, 'sex':user.usersex,'addon':timeinfo(user.useraddon)}
    return render_template('profile.html', user=user)

@app.route('/profiles', methods=["GET", "POST"])
def profiles():
  users = db.session.query(User).all()
  if request.method == "POST" or ('Content-Type' in request.headers and request.headers['Content-Type'] == 'application/json'):
    userlist=[]
    for user in users:
      userlist.append({'id':user.id,'username':user.username})
    return jsonify(users=userlist)
  else:
    return render_template('profiles.html', users=users)

def timeinfo(entry):
    day = time.strftime("%a")
    date = time.strftime("%d")
    if (date <10):
        date = date.lstrip('0')
    month = time.strftime("%b")
    year = time.strftime("%Y")
    return day + ", " + date + " " + month + " " + year

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
