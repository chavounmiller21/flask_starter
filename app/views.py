"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app,db
from flask import render_template, request, redirect, url_for, flash, send_from_directory,session
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import NewPropertyForm


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
    return render_template('about.html', name="Mary Jane")

@app.route("/properties/create", methods=['POST','GET'])
def createproperty():
    form = NewPropertyForm()
    if (request.method == 'POST'):
        if (form.validate_on_submit()):
            img = form.photo.data
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            db.session.add(Property(form.title.data, form.description.data, form.number_of_bedrooms.data, form.number_of_bathrooms.data, 
                                    form.location.data, form.price.data, form.property_type.data, filename))
            db.session.commit()
            flash('Property Succesfully added!')
            return redirect(url_for('listofproperties'))
        else:
            flash_errors(form)
    return render_template('create-property.html', form=form)
   
@app.route("/properties")         
def listofproperties():
    pro= Property.query.all()
    return render_template('properties.html', pro = pro)

@app.route("/properties/<propertyid>")  
def getproperty(propertyid):
    id = Property.query.filter_by(id=propertyid).first()
    return render_template('property.html', id = id)

@app.route('/uploads/<filename>')
def get_images(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"]), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404