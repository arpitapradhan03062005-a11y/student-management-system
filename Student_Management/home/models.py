from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('Computer Engineering', 'Computer Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Electronics Engineering', 'Electronics Engineering'),
    ]

    SEMESTER_CHOICES = [
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
        ('7', 'Semester 7'),
        ('8', 'Semester 8'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile",
    )

    roll_number = models.CharField(max_length=20, unique=True)

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+?[\d\s\-\(\)]{10,17}$',
        message="Enter a valid phone number (digits, spaces, dashes, and parentheses allowed)."
    )

    phone = models.CharField(validators=[phone_regex], max_length=15)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES
    )

    date_of_birth = models.DateField()

    admission_date = models.DateField(auto_now_add=True)

    address = models.TextField()

    photo = models.ImageField(
        upload_to='student_photos/',
        blank=True,
        null=True  
    )

    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)

    emergency_contact = models.CharField(validators=[phone_regex], max_length=15, blank=True)

    student_signature = models.ImageField(
        upload_to='signatures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    

class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
    

class Subject(models.Model):

    name = models.CharField(max_length=100)

    department = models.CharField(
        max_length=50,
        choices=Student.DEPARTMENT_CHOICES,
    )

    semester = models.CharField(
        max_length=10,
        choices=Student.SEMESTER_CHOICES,
    )

    max_marks = models.PositiveIntegerField(default=100)

    class Meta:
        unique_together = ('name', 'department', 'semester')

    def __str__(self):
        return f"{self.name} ({self.department} - Sem {self.semester})"


class Result(models.Model):

    EXAM_TYPE_CHOICES = [
        ('Midterm', 'Midterm'),
        ('Final', 'Final'),
        ('Assignment', 'Assignment'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="results",
    )

    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='Final')

    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)

    entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('student', 'subject', 'exam_type')
        ordering = ['subject__name']

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} - {self.marks_obtained}"

    @property
    def percentage(self):
        if self.subject.max_marks:
            return round((float(self.marks_obtained) / self.subject.max_marks) * 100, 1)
        return 0