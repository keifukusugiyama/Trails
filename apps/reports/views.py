from django.shortcuts import render, redirect
from apps.login_reg_app.models import Users #to use Users table for user id
from apps.trail_app.models import Trails 
from django.contrib import messages #for flash message

def user_report(request, id):
    user_id= Users.objects.get(id=id)
    context={
        "reports" : Reports.objects.filter (user_id= id),
        "user_name": user_id.first_name
    }
    return render(request, "reports/user_reports.html", context)

# process creating new review
def create_report(request):
    if request.method == "POST":
        user = Users.objects.get(id=request.session['user_id'])
        book = Books.objects.get(id= request.POST['book_id'])
        # create new review with link to user and book objects
        new_review = Reviews.objects.create(comment = request.POST['comment'], rating = int(request.POST['rating']), book_id = book, user_id = user)
        # go back to book info page
        return redirect(f"/books/{book.id}")

# delete review post and return to book page
def delete_report(request, id):
    if request.method == "POST":
        this_review = Reviews.objects.get(id= request.POST['review_id'])
        this_review.delete()
        book = Books.objects.get(id= id)
        return redirect(f"/books/{book.id}")

# show edit review form
def edit_report(request, id):
    context = {
        "this_review": Reviews.objects.get(id=id)
    }
    return render(request, "books_app/edit_review.html", context)

# process updating review
def update_report(request, id):
    if request.method == "POST":
        this_review = Reviews.objects.get(id=id)
        this_review.comment = request.POST['comment']
        this_review.rating = request.POST['rating']
        this_review.save()

        return redirect(f"/books/{this_review.book_id.id}")