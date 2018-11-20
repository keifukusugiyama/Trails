from django.shortcuts import render, redirect
from apps.login_reg_app.models import Users #to use Users table for user id
from apps.trail_app.models import Trails 
from apps.reports.models import Reports 
from django.contrib import messages #for flash message

def user_report(request, id):
    user_id= Users.objects.get(id=id)
    context={
        "reports" : Reports.objects.filter (user_id= id),
        "user_name": user_id.first_name,
        "wish_list_trails": Trails.objects.filter(wish_list_users = id)
    }
    return render(request, "reports/user_reports.html", context)

# process creating new report
def create_report(request):
    if request.method == "POST":
        user = Users.objects.get(id=request.session['user_id'])
        trail = Trails.objects.get(id= request.POST['trail_id'])

        new_report = Reports.objects.create(comment = request.POST['comment'], rating = request.POST['rating'], trail_id = trail, user_id = user)

        return redirect(f"/trails/{trail.id}")

# delete report post and return to book page
def delete_report(request):
    if request.method == "POST":
        this_report = Reports.objects.get(id= request.POST['report_id'])
        this_report.delete()
        return redirect(f"/trails/{this_report.trail_id.id}")

# show edit report form
def edit_report(request, id):
    context = {
        "this_report": Reports.objects.get(id=id)
    }
    return render(request, "reports/edit_report.html", context)

# process updating report
def update_report(request, id):
    if request.method == "POST":
        this_report = Reports.objects.get(id=id)
        this_report.comment = request.POST['comment']
        this_report.rating = request.POST['rating']
        this_report.save()

        return redirect(f"/reports/user/{this_report.user_id.id}")