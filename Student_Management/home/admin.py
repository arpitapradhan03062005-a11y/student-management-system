from django.contrib import admin
from .models import Student, Attendance, Subject,Result

# Register your models here.
admin.site.register(Student)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date')
    search_fields = ('student__name', 'student__roll_number')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'semester', 'max_marks')
    list_filter = ('department', 'semester')
    search_fields = ('name',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_type', 'marks_obtained', 'entered_by')
    list_filter = ('exam_type', 'subject__department', 'subject__semester')
    search_fields = ('student__name', 'student__roll_number', 'subject__name')