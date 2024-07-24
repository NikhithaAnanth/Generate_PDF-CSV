
import csv
from django.http import HttpResponse
from .models import Student
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import render
from django.http import JsonResponse
from .forms import StudentForm

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = StudentForm()
    return render(request, 'enrollment/register.html', {'form': form})

def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'USN'])

    students = Student.objects.all()
    for student in students:
        writer.writerow([student.first_name, student.last_name, student.email, student.USN])

    return response

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Student Enrollment List")
    p.drawString(100, 735, "------------------------")

    students = Student.objects.all()
    y = 700
    for student in students:
        p.drawString(100, y, f'{student.first_name} {student.last_name} - {student.email} - {student.USN}')
        y -= 20

    p.showPage()
    p.save()
    return response
