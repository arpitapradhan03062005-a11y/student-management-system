from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Student, Attendance, Subject, Result
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentForm
from datetime import date
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q, Count
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.colors import HexColor, white
from django.core.paginator import Paginator
# Create your views here.
# def home(request):

#     return render(request,"home.html")
def home(request):

    total_students = Student.objects.count()

    male_students = Student.objects.filter(gender="Male").count()
    female_students = Student.objects.filter(gender="Female").count()

    departments = Student.objects.values("department").distinct().count()
    semesters = Student.objects.values("semester").distinct().count()

   #department chart
    dept_counts_qs = dict(
        Student.objects.values_list("department").annotate(n=Count("id"))
    )

    labels = []
    counts = []

    for dept, _ in Student.DEPARTMENT_CHOICES:
        labels.append(dept)
        counts.append(dept_counts_qs.get(dept, 0))

    # Semester Chart
    sem_counts_qs = dict(
        Student.objects.values_list("semester").annotate(n=Count("id"))
    )

    sem_labels = []
    sem_counts = []

    for sem, label in Student.SEMESTER_CHOICES:
        sem_labels.append(label)
        sem_counts.append(sem_counts_qs.get(sem, 0))

    context = {
        "total_students": total_students,
        "male_students": male_students,
        "female_students": female_students,
        "departments": departments,
        "semesters": semesters,
        "recent_students": Student.objects.order_by("-id")[:5],
        "today": date.today(),
        "dept_labels": json.dumps(labels),
        "dept_counts": json.dumps(counts),
        "sem_labels": json.dumps(sem_labels),
        "sem_counts": json.dumps(sem_counts),

    }

    return render(request, "home.html", context)


def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Send welcome email
        try:
            send_mail(
                subject="Welcome to Student Management System",
                message=f"""Hello {user.username},

Your account has been created successfully.

Thank you for registering with our Student Management System.

Happy Learning!

Regards,
Student Management Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception:
            messages.warning(request, "Account created, but email could not be sent.")

        messages.success(request, "Registration successful! Please login.")

        return redirect("login")

    return render(request, "register.html")

# def login_user(request):

#     if request.method=="POST":

#         username=request.POST.get("username")

#         password=request.POST.get("password")

#         user=authenticate(

#             username=username,

#             password=password

#         )

#         if user is not None:

#             login(request,user)

#             return redirect("home")

#         else:

#             messages.error(request, "Invalid username or password.")

#     return render(request,"login.html")

def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            if user.groups.filter(name='Admin').exists():
                return redirect('dashboard')

            elif user.groups.filter(name='Teacher').exists():
                return redirect('teacher_dashboard')

            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')

            else:
                return redirect('home')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect("login")

@login_required

def profile(request):

    return render(request,"profile.html")

@login_required
def add_student(request):

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Student saved successfully!")
            return redirect("view_student")

    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})


@login_required
def view_student(request):

    students = Student.objects.all()

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    search = request.GET.get("search")
    department = request.GET.get("department")
    semester = request.GET.get("semester")
    gender = request.GET.get("gender")

    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(roll_number__icontains=search)
        )

    if department:
        students = students.filter(department=department)

    if semester:
        students = students.filter(semester=semester)

    if gender:
        students = students.filter(gender=gender)

    paginator = Paginator(students, 25)  # 25 students per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "students": page_obj,
        "page_obj": page_obj,
        "departments": Student.DEPARTMENT_CHOICES,
        "semesters": Student.SEMESTER_CHOICES,
        "genders": Student.GENDER_CHOICES,
    }

    return render(request, "view_student.html", context)

@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")
    student.delete()

    messages.success(request, "Student deleted successfully!")

    return redirect("view_student")

@login_required
def update_student(request, id):

    student = get_object_or_404(Student, id=id)

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("view_student")

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "update_student.html",
        {"form": form}
    )

@login_required
def student_detail(request, id):

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    student = get_object_or_404(Student, id=id)

    return render(
        request,
        "student_detail.html",
        {"student": student}
    )

@login_required
def student_id_card(request, id):

    student = get_object_or_404(Student, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.roll_number}_ID_Card.pdf"'

    p = canvas.Canvas(response)
    p.setPageSize((350, 260))

    # Border
    p.rect(10, 10, 330, 240)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(175, 230, "STUDENT ID CARD")

    # Student Photo
    if student.photo:
        try:
            photo = ImageReader(student.photo.path)
            p.drawImage(photo, 20, 125, width=70, height=80)
        except:
            pass

    # Student Details
    p.setFont("Helvetica", 11)

    p.drawString(110, 200, f"Name : {student.name}")
    p.drawString(110, 180, f"Roll No : {student.roll_number}")
    p.drawString(110, 160, f"Department : {student.department}")
    p.drawString(110, 140, f"Semester : {student.semester}")
    p.drawString(20, 105, f"Blood Group : {student.blood_group or '—'}")
    p.drawString(20, 90, f"Emergency Contact : {student.emergency_contact or '—'}")

    # Signature
    if student.student_signature:
        try:
            sig = ImageReader(student.student_signature.path)
            p.drawImage(sig, 20, 35, width=90, height=35)
            p.setFont("Helvetica", 8)
            p.drawCentredString(65, 28, "Signature")
        except:
            pass

    # Generate QR Code
    qr = qrcode.make(f"Name: {student.name}\nRoll: {student.roll_number}")

    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    qr_image = ImageReader(buffer)

    p.drawImage(qr_image, 250, 30, width=70, height=70)

    p.save()

    return response

@login_required
def teacher_dashboard(request):

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    total_students = Student.objects.count()
    male_students = Student.objects.filter(gender="Male").count()
    female_students = Student.objects.filter(gender="Female").count()

    context = {
        "total_students": total_students,
        "male_students": male_students,
        "female_students": female_students,
        "recent_students": Student.objects.order_by("-id")[:5],
    }

    return render(request, 'teacher_dashboard.html', context)

@login_required
def student_dashboard(request):

    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = None

    attendance_records = []
    attendance_percentage = None
    results = []
    overall_percentage = None

    if student is not None:
        attendance_records = student.attendance_records.all()[:30]

        total_marked = student.attendance_records.count()
        present_count = student.attendance_records.filter(status__in=["Present", "Late"]).count()

        if total_marked > 0:
            attendance_percentage = round((present_count / total_marked) * 100, 1)

        results = student.results.select_related('subject').all()

        if results:
            total_obtained = sum(float(r.marks_obtained) for r in results)
            total_max = sum(r.subject.max_marks for r in results)
            if total_max > 0:
                overall_percentage = round((total_obtained / total_max) * 100, 1)

    else:
        messages.warning(request, "Your account is not linked to a student record yet. Please contact the administrator.")

    context = {
        "student": student,
        "attendance_records": attendance_records,
        "attendance_percentage": attendance_percentage,
        "results": results,
        "overall_percentage": overall_percentage,
    }

    return render(request, 'student_dashboard.html', context)

@login_required
def mark_attendance(request):

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    selected_date = request.POST.get("date") or request.GET.get("date") or str(date.today())
    department = request.GET.get("department", "")

    students = Student.objects.all()
    if department:
        students = students.filter(department=department)

    if request.method == "POST":

        for student in students:
            status = request.POST.get(f"status_{student.id}")
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={"status": status, "marked_by": request.user},
                )

        messages.success(request, f"Attendance saved for {selected_date}.")
        return redirect(f"/attendance/mark/?date={selected_date}&department={department}")

    # Pre-fill existing attendance for that date, so re-opening the page shows what's already saved
    existing = {
        a.student_id: a.status
        for a in Attendance.objects.filter(date=selected_date, student__in=students)
    }

    context = {
        "students": students,
        "selected_date": selected_date,
        "department": department,
        "departments": Student.DEPARTMENT_CHOICES,
        "existing": existing,
    }

    return render(request, "mark_attendance.html", context)

@login_required
def enter_marks(request):

    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return HttpResponse("Permission Denied")

    subject_id = request.POST.get("subject") or request.GET.get("subject", "")
    exam_type = request.POST.get("exam_type") or request.GET.get("exam_type", "Final")

    subjects = Subject.objects.all()
    students = []

    if subject_id:
        subject = get_object_or_404(Subject, id=subject_id)
        students = Student.objects.filter(
            department=subject.department,
            semester=subject.semester,
        )

    if request.method == "POST" and subject_id:

        for student in students:
            marks = request.POST.get(f"marks_{student.id}")
            if marks:
                Result.objects.update_or_create(
                    student=student,
                    subject_id=subject_id,
                    exam_type=exam_type,
                    defaults={"marks_obtained": marks, "entered_by": request.user},
                )

        messages.success(request, "Marks saved successfully.")
        return redirect(f"/results/enter/?subject={subject_id}&exam_type={exam_type}")

    existing = {}
    if subject_id:
        existing = {
            r.student_id: r.marks_obtained
            for r in Result.objects.filter(subject_id=subject_id, exam_type=exam_type)
        }

    context = {
        "subjects": subjects,
        "students": students,
        "selected_subject": subject_id,
        "exam_type": exam_type,
        "exam_types": Result.EXAM_TYPE_CHOICES,
        "existing": existing,
    }

    return render(request, "enter_marks.html", context)
