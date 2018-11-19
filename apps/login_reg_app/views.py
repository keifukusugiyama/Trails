from django.shortcuts import render, redirect
from .models import Users #for user data table
from django.contrib import messages #for flash message
import bcrypt #for password hash

def index(request):
    # if user is already logged in, return to trails
    if "user_id" in request.session:
        return redirect("/trails")
        # otherwise, show login/reg page
    return render(request, "login_reg_app/index.html")

def create(request):
    if request.method == "POST":
        #basic_validator in models.py generates errors
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
        else:
            #if there's no error, hash the password
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            #create new user
            new_user = Users.objects.create(first_name= request.POST['fname'], last_name= request.POST['lname'], email= request.POST['email'], password= hash1.decode())
            #save newly created user id in session
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.first_name
            return redirect("/trails")

def login(request):
    if request.method == "POST":
        # get list of user object that matches email field
        user = Users.objects.filter(email = request.POST['email'])
        # if there is a match, check email and login
        if len(user) > 0:
            if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
                # to store user id in session
                request.session['user_id'] = user[0].id
                request.session['user_name'] = user[0].first_name
                return redirect("/trails")
        # if there's no match for email or if the password don't match, error
        messages.error(request, "Login Failed")
        return redirect("/")
        
def logout(request):
    request.session.clear()
    return redirect('/')

def myaccount(request, id):
    if int(id) != int(request.session['user_id']):
        return redirect("/trails")

    context ={
        "this_user": Users.objects.get(id=id)
    }
    return render(request, "login_reg_app/myaccount.html", context)

def update(request, id):
    if request.method == "POST":
        this_user = Users.objects.get(id=id)
        errors = Users.objects.edit_validator(request.POST, id)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/myaccount/{request.session['user_id']}")
        else:
            this_user.first_name = request.POST['fname']
            this_user.last_name = request.POST['lname']
            this_user.email = request.POST['email']
            this_user.save()

    return redirect("/trails")