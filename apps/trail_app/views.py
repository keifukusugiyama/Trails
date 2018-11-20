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

def create_trail(request):
    if request.method == "POST":
        errors = Trails.objects.trail_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trails')
        else:
            user = Users.objects.get(id=request.session['user_id'])
            new_trail = Trails.objects.create(name=request.POST['name'], length=request.POST['length'], elevation=request.POST['elevation'], level=request.POST['level'], trail_head=request.POST['trail_head'], link=request.POST['link'], user_id=user)

        return redirect(f"/trails/{new_trail.id}")

def view_trail(request, id):
    context={
        "trail" : Trails.objects.get(id= id),
        "reports" : Reports.objects.filter (trail_id= id)
    }
    return render(request, "trail_app/trail_info.html", context)

def delete_trail(request):
    if request.method == "POST":
        this_trail = Trails.objects.get(id= request.POST['trail_id'])
        this_trail.delete()
        return redirect('/trails')

def edit_trail(request, id):
    context = {
        "trail": Trails.objects.get(id=id)
    }
    return render(request, "trail_app/edit_trail.html", context)

def update_trail(request, id):
    if request.method == "POST":
        errors = Trails.objects.trail_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/trails/{id}')

        this_trail = Trails.objects.get(id=id)
        this_trail.name = request.POST['name']
        this_trail.length = request.POST['length']
        this_trail.elevation = request.POST['elevation']
        this_trail.level = request.POST['level']
        this_trail.trail_head = request.POST['trail_head']
        this_trail.link = request.POST['link']
        this_trail.save()

        return redirect(f"/trails/{this_trail.id}")