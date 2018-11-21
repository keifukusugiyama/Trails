from django.shortcuts import render, redirect
from apps.login_reg_app.models import Users #to use Users table for user id
from apps.trail_app.models import Trails 
from apps.reports.models import Reports, Exercises, Comments 
from django.contrib import messages #for flash message

def user_report(request, id):
    user_id= Users.objects.get(id=id)
    context={
        "reports" : Reports.objects.filter(user_id= id).order_by('-updated_at'),
        "user_name": user_id.first_name,
        "wish_list_trails": Trails.objects.filter(wish_list_users = id),
    }
    return render(request, "reports/user_reports.html", context)

def new_report(request, id):
	context={
		'trail' : Trails.objects.get(id=id)
	}
	return render(request, "reports/new_report.html", context)

# process creating new report
def create_report(request):
    if request.method == "POST":
		# saving user and trail for foreign key
        user = Users.objects.get(id=request.session['user_id'])
        trail = Trails.objects.get(id= request.POST['trail_id'])

		# validate reports fields
        errors = Reports.objects.report_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/reports/{trail.id}/new_report")
		# if there's no error, add new report
        new_report = Reports.objects.create(comment = request.POST['comment'], rating = request.POST['rating'], trail_id = trail, user_id = user)

		#if user said yes to adding exercise log
        if request.POST['log_exercise'] == "yes":
			# validate exercise fields
            errors2 = Exercises.objects.exercise_validator(request.POST)
            if len(errors2) > 0:
                for key, value in errors2.items():
                    messages.error(request, value)
                return redirect(f"/reports/{trail.id}/new_report")
			# if there's no error, add new exercise
            new_exercise = Exercises.objects.create(duration = request.POST['duration'], avg_bpm = request.POST['avg_bpm'], max_bpm = request.POST['max_bpm'], calories = request.POST['calories'], pace = request.POST['pace'], steps = request.POST['steps'], elevation = request.POST['elevation'], report_id = new_report, user_id = user)

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

def new_comment(request, id):
    if request.method == "POST":
        this_report = Reports.objects.get(id= id)
        user = Users.objects.get(id=request.session['user_id'])

        new_comment = Comments.objects.create(comment_text = request.POST['comment_text'], report_id = this_report, user_id = user)

        return redirect(f"/reports/user/{this_report.user_id.id}")