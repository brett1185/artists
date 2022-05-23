from flask import render_template,redirect,session,request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.picture import Picture

@app.route('/pictures/new')
def add_painting():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    return render_template('add_painting.html', user=User.get_by_id(data))

@app.route('/create/picture', methods = ["POST"])
def create_painting():
    if 'user_id'not in session:
        return redirect('/logout')
    if not Picture.validate_picture(request.form):
        return redirect('/pictures/new')
    data={ 
        'title':request.form['title'],
        'description':request.form['description'],
        'price':int(request.form['price']),
        'user_id':session['user_id']
    }
    Picture.save(data)
    return redirect('/dashboard')

@app.route('/paintings/<int:id>')
def picture_info(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    user_data={
        'id':session['user_id']
    }
    return render_template('show_painting.html', paintings=Picture.get_one(data), user=User.get_by_id(user_data))

@app.route('/edit/picture/<int:id>')
def edit_picture(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':id
    }
    user_data={
        'id':session['user_id']
    }
    return render_template('edit_painting.html', edit=Picture.get_one(data), user=User.get_by_id(user_data))

@app.route('/update/picture', methods =['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Picture.validate_picture(request.form):
        return redirect('/edit/picture')
    data = {
        'title':request.form['title'],
        'description':request.form['description'],
        'price':int(request.form['price']),
    }
    Picture.update(data)
    return redirect('/dashboard')

@app.route('/delete/picture/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Picture.delete(data)
    return redirect('/dashboard')