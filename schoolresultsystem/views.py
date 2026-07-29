from urllib import request
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from schoolresultsystem.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
# Create your views here.
def index(request):
    notices = Notice.objects.all().order_by('-posting_date')
    context = {'notices': notices,}
    return render(request, 'index.html', context)

def admin_login(request):   
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    else:
        error=None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password'
    return render(request, 'admin_login.html',locals())
@login_required
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    total_student=Student.objects.count()
    total_subject=Subject.objects.count()
    total_class=Class.objects.count()
    total_result=Result.objects.values('student').distinct().count()
    return render(request, 'admin_dashboard.html',locals())

def admin_logout(request):
    logout(request)
    return redirect('admin_login')
@login_required
def create_class(request):
    if request.method == 'POST':
       try:
           class_name = request.POST.get('class_name')
           class_numeric = request.POST.get('class_name_numeric')
           section = request.POST.get('Section')
           Class.objects.create(class_name=class_name, class_numeric=class_numeric, section=section)
           messages.success(request, "Class created successfully.")
           return redirect('create_class')  # Redirect to the same page after successful creation
       except Exception as e: 
           messages.error(request, f"An error occurred: {str(e)}")
           return redirect('create_class')  # Redirect to the same page after error
    return render(request, 'Admin/Class/create_class.html')

@login_required
def manage_class(request):
   classes = Class.objects.all()
   if request.GET.get('delete'):
        try:
            class_id = request.GET.get('delete')
            class_obj=get_object_or_404(Class,pk=class_id)
            class_obj.delete()
            messages.success(request,"class deleted successful")
            return redirect('manage_class')
        except Exception as e:
             messages.error(request, f"An error occurred: {str(e)}")
             return redirect('manage_class')
               
   return render(request, 'Admin/Class/manage_class.html',locals())

@login_required
def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        class_numeric = request.POST.get("class_name_numeric")
        section = request.POST.get("Section")
        try:
            class_obj.class_name = class_name
            class_obj.class_numeric = class_numeric
            class_obj.section = section
            class_obj.save()
            messages.success(request, "Class updated successfully.")
            return redirect("manage_class")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request,"Admin/Class/edit_class.html",{"class_obj": class_obj})


@login_required
def create_subject(request):
    if request.method == 'POST':
       try:
           subject_name = request.POST.get('subject_name')
           subject_code = request.POST.get('subject_code')
           Subject.objects.create(subject_name=subject_name, subject_code=subject_code)
           messages.success(request, "Subject created successfully.")
       except Exception as e: 
           messages.error(request, f"An error occurred: {str(e)}")
       return redirect('create_subject')  # Redirect to the same page after error
    return render(request, 'Admin/Subjects/create_subject.html')


@login_required
def manage_subject(request):
   subjects = Subject.objects.all()
   if request.GET.get('delete'):
        try:
            Subject_id = request.GET.get('delete')
            subject_obj=get_object_or_404(Subject,pk=Subject_id)
            subject_obj.delete()
            messages.success(request,"subject deleted successful")
        except Exception as e:
             messages.error(request, f"An error occurred: {str(e)}")
        return redirect('manage_subject')
   return render(request, 'Admin/Subjects/manage_subject.html',locals())


@login_required
def subject_edit(request,subject_id):
    subject_obj = get_object_or_404(Subject,pk=subject_id)
    if request.method == 'POST':
           subject_name = request.POST.get('subject_name')
           subject_code = request.POST.get('subject_code')
           try:
                subject_obj.subject_name = subject_name
                subject_obj.subject_code = subject_code
                subject_obj.save()
                messages.success(request, "Subject updated successfully.")
           except Exception as e: 
                messages.error(request, f"An error occurred: {str(e)}")
           return redirect('manage_subject')  
    return render(request, 'Admin/Subjects/subject_edit.html',locals())


@login_required
def subject_combination(request):
    classes=Class.objects.all()
    subjects=Subject.objects.all()
    if request.method == 'POST':
       try:
           class_id = request.POST.get('class')
           subject_id = request.POST.get('subject')
           Subjectcombination.objects.create(student_class_id=class_id,subjects_id=subject_id,status=1)
           messages.success(request, "Subject combination successfully.")
       except Exception as e: 
           messages.error(request, f"An error occurred: {str(e)}")
       return redirect('subject_combination')  # Redirect to the same page after error
    return render(request, 'Admin/Subjects/subject_combination.html',locals())


@login_required
def manage_subject_combination(request):
    combinations = Subjectcombination.objects.select_related("student_class","subjects").all()
    aid = request.GET.get("aid")
    did = request.GET.get("did")
    if aid:
        try:
            Subjectcombination.objects.filter(id=aid).update(status="1")
            messages.success(request, "Subject combination activated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect("manage_subject_combination")

    if did:
        try:
            Subjectcombination.objects.filter(id=did).update(status="0")
            messages.success(request, "Subject combination deactivated successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect("manage_subject_combination")

    return render(request,"Admin/Subjects/manage_subject_combination.html",{"combinations": combinations})



@login_required
def Add_student(request):
    classes=Class.objects.all()
    if request.method == 'POST':
       try:
           name = request.POST.get('fullname')
           roll_id = request.POST.get('rollid')
           email_id = request.POST.get('emailid')
           gender_id = request.POST.get('gender')
           dob_id = request.POST.get('dob')
           class_id = request.POST.get('class')
           Student.objects.create(name=name,roll_id=roll_id,Email=email_id,gender=gender_id,Date_of_birth=dob_id,Student_class_id=class_id)
           messages.success(request, "Add Student successfully.")
       except Exception as e: 
           messages.error(request, f"An error occurred: {str(e)}")
       return redirect('Add_student')  # Redirect to the same page after error
    return render(request, 'Admin/Students/create_student.html',locals())



@login_required
def manage_student(request):
   students = Student.objects.all()
   return render(request, 'Admin/Students/manage_student.html',locals())



@login_required
def edit_student(request, student_id):
    student_obj = get_object_or_404(Student, pk=student_id)
    classes = Class.objects.all()
    if request.method == "POST":
        try:
            student_obj.name = request.POST.get("fullname")
            student_obj.roll_id = request.POST.get("rollid")
            student_obj.Email = request.POST.get("email")
            student_obj.gender = request.POST.get("gender")
            student_obj.Date_of_birth = request.POST.get("dob")
            class_id = request.POST.get("class")
            if class_id:
                student_obj.Student_class = get_object_or_404(Class, pk=class_id)
            student_obj.Status = request.POST.get("Status")
            student_obj.save()
            messages.success(request, "Student updated successfully.")
            return redirect("manage_student")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    context = {"student_obj": student_obj,"classes": classes,}
    return render(request, "Admin/Students/edit_student.html", context)


@login_required
def Add_Notice(request):
    notice=Notice.objects.all()
    if request.method == 'POST':
       try:
           title = request.POST.get('title')
           details = request.POST.get('details')
           Notice.objects.create(title=title,details=details)
           messages.success(request, "Add Notice successfully.")
       except Exception as e: 
           messages.error(request, f"An error occurred: {str(e)}")
       return redirect('Add_Notice')  # Redirect to the same page after error
    return render(request, 'Admin/Notice/Add_Notice.html',locals())


@login_required
def manage_notice(request):
   notice = Notice.objects.all()
   if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_obj=get_object_or_404(Notice,pk=notice_id)
            notice_obj.delete()
            messages.success(request,"notice deleted successful")
        except Exception as e:
             messages.error(request, f"An error occurred: {str(e)}")
        return redirect('manage_notice')
   return render(request, 'Admin/Notice/Manage_notice.html',locals())


@login_required
def Add_result(request):
    classes = Class.objects.all()
    if request.method == "POST":
        try:
            student_id = request.POST.get("student_id")
            class_id = request.POST.get("class")
            student = Student.objects.get(id=student_id)
            subjects = Subjectcombination.objects.filter( student_class_id=class_id )
            for subject in subjects:
                marks = request.POST.get(f"marks_{subject.subjects.id}")
                if marks:
                    Result.objects.create(student=student, student_class_id=class_id, subjects=subject.subjects, marks=int(marks))
            messages.success(request, "Result added successfully.")
            return redirect("Add_result")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request, "Admin/Results/Add_result.html",locals())

def get_students_subjects(request):
    class_id = request.GET.get("class_id")
    students = list(Student.objects.filter(Student_class_id=class_id).values("id","name","roll_id"))
    subjects = list(Subjectcombination.objects.filter(student_class_id=class_id).values("subjects__id","subjects__subject_name"))
    subject_list = []
    for s in subjects:
        subject_list.append({"id": s["subjects__id"],"name": s["subjects__subject_name"]})
    return JsonResponse({"students": students,"subjects": subject_list})
    
    


@login_required
def manage_result(request):
    results = Result.objects.select_related('student','student_class').all()
    students = {}
    for res in results:
        stu_id = res.student.id
        # Only add each student once
        if stu_id not in students:
            students[stu_id] = {'student': res.student,'class': res.student_class,}
    context = {'results': students.values()}
    return render(request, 'Admin/Results/manage_result.html', context)
       


@login_required
def edit_result(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    results = Result.objects.select_related('student','student_class','subjects').filter(student=student)
    if request.method == "POST":
        for result in results:
            marks = request.POST.get(f"marks_{result.id}")
            if marks:
                result.marks = int(marks)
                result.save()
        messages.success(request, "Result updated successfully.")
        return redirect("manage_result")
    context = {"student": student,"results": results,}
    return render(request, "Admin/Results/edit_result.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        user = request.user
        # Check current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")
        # Check new passwords match
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("change_password")
        # Password length validation
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("change_password")
        # Save new password
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Password changed successfully.")
        return redirect("change_password")
    return render(request, "Admin/change_password/change_password.html")       


def student_login(request):
    classes = Class.objects.all()
    if request.method == "POST":
        roll_id = request.POST.get("roll_id")
        class_id = request.POST.get("class")
        try:
            student = Student.objects.get(roll_id=roll_id,Student_class_id=class_id)
            request.session["student_id"] = student.id
            return redirect("student_result")
        except Student.DoesNotExist:
            messages.error(request, "Invalid Roll ID or Class.")
    return render(request, "student_login.html", {"classes": classes})


def student_result(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_login")
    student = Student.objects.get(id=student_id)
    results = Result.objects.select_related("subjects").filter(student=student)
    return render(request,"student_result.html",{"student": student,"results": results,},)