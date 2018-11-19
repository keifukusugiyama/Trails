from django.shortcuts import render, redirect
from apps.login_reg_app.models import Users #to use Users table for user id
from apps.trail_app.models import Trails 
from apps.reports.models import Reports 
from django.contrib import messages #for flash message

# Main Books page
def trails_main(request):
    #if user is not logged in, return to login/reg
    if "user_id" not in request.session: 
        return redirect("/")

    context={
        'all_reports': Reports.objects.all().order_by('-updated_at')[:3],
        'all_trails': Trails.objects.all()
    }
    return render(request, "trail_app/trails.html", context)


# process creating new book and new review associated
def create_trail(request):
    if request.method == "POST":
        # create new book
        new_book = Books.objects.create(title=request.POST['title'], author=request.POST['author'])

        # getting current user's object
        user = Users.objects.get(id=request.session['user_id'])
        # create new review with link to user and book objects
        new_review = Reviews.objects.create(comment = request.POST['comment'], rating = int(request.POST['rating']), book_id = new_book , user_id = user)
        # go to new book info page
        return redirect(f"/books/{new_book.id}")

# show book info page with book info and reviews 
def view_trail(request, id):
    context={
        "book" : Books.objects.get(id= id),
        "reviews" : Reviews.objects.filter (book_id= id)
    }
    return render(request, "books_app/book_info.html", context)

def delete_trail(request, id):
    if request.method == "POST":
        this_review = Reviews.objects.get(id= request.POST['review_id'])
        this_review.delete()
        book = Books.objects.get(id= id)
        return redirect(f"/books/{book.id}")

# show edit review form
def edit_trail(request, id):
    context = {
        "this_review": Reviews.objects.get(id=id)
    }
    return render(request, "books_app/edit_review.html", context)

# process updating review
def update_trail(request, id):
    if request.method == "POST":
        this_review = Reviews.objects.get(id=id)
        this_review.comment = request.POST['comment']
        this_review.rating = request.POST['rating']
        this_review.save()

        return redirect(f"/books/{this_review.book_id.id}")