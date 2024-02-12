# main.views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView 



from django.urls import reverse_lazy

from .models import Course, TimeTable, Seat, Hall
from .forms import CourseForm, TimeTableForm, SeatForm, HallForm
from accounts.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin
import csv

import random
from .utils import get_today_courses

from datetime import datetime, timedelta
from datetime import timedelta
from itertools import zip_longest
from .models import Course, TimeTable, Seat, Course, Hall

from more_itertools import interleave_evenly

import random

from django.views import View
from django.shortcuts import render
from more_itertools import interleave_evenly


    
from .mixins import AdminRequiredMixin
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve TimeTable data and pass it to the template
        context['timetable_data'] = TimeTable.objects.all()
        return context
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def hall_seats_view(request):
    all_halls = Hall.objects.all()

    hall_seat_data = {}

    for hall in all_halls:
        seats_in_hall = Seat.objects.filter(hall=hall)
        hall_seat_data[hall] = seats_in_hall

    context = {'hall_seat_data': hall_seat_data}
    return render(request, 'main/hall_seats.html', context)


class AllocateSeatsView(AdminRequiredMixin, View):
    template_name = 'main/allocations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Seat.objects.all().update(student=None)
        
        all_halls = Hall.objects.all()
        all_courses = Course.objects.all()
        
        courses_today = get_today_courses()
        
        students_by_course = {}
        stud_by_co = []
        for course in courses_today:
            students_in_course = Student.objects.filter(offer__course=course)
            students_by_course[course.name] = list(students_in_course)
            stud_by_co.append(tuple(students_in_course))
        
        
        if not stud_by_co:
            context = {'message': "There are no exams sheduled for today"}
            return render(request, self.template_name, context)
            
        shuffled_students = list(interleave_evenly(stud_by_co))
        
        hall_seat_data = {}
        
        for hall in all_halls:
            seats_in_hall = Seat.objects.filter(hall=hall)
            hall_seat_data[hall] = seats_in_hall
            
       
        for hall, seats_queryset in hall_seat_data.items():
            students = iter(shuffled_students)
            
            for seat in seats_queryset:
                try:
                    student = next(students)
                    seat.student = student
                    seat.save()
                except StopIteration:
                    # No more students to assign
                    seat.student = None
                    seat.save()

        # If there are remaining students or seats, handle them accordingly
        remaining_students = list(students)
        remaining_seats = Seat.objects.filter(hall=hall).exclude(id__in=[seat.id for seat in seats_queryset])

        for seat, student in zip(remaining_seats, remaining_students):
            seat.student = student
            seat.save()
        context = {'hall_seat_data': hall_seat_data}
        return render(request, 'main/hall_seats.html', context)
    
    
class AdminDashboardView(AdminRequiredMixin, FormView):
    template_name = 'main/admin_dashboard.html'
    form_class = CourseForm 
    success_url = '/admin/dashboard/'
    def get_form(self, form_class=None):
        form_type = self.request.GET.get('form_type', 'course')
        if form_type == 'course':
            self.form_class = CourseForm
        elif form_type == 'timetable':
            self.form_class = TimeTableForm
        elif form_type == 'seat':
            self.form_class = SeatForm
        elif form_type == 'hall':
            self.form_class = HallForm
        return super().get_form(form_class)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = self.request.GET.get('form_type', 'course')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    

class CourseCreateView(AdminRequiredMixin, View):
    template_name = 'main/courses.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        form = CourseForm()
        return render(request, self.template_name, {'courses': courses, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:courses')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            print(row, "row ....")
            Course.objects.create(name=row['name'], code=row['code'], department_id=row['department_id'])

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:courses')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:courses')

        return render(request, self.template_name, {'form': form})
    

class GenerateTimeTableView(AdminRequiredMixin, View):
    template_name = 'main/timetables.html'
    
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        timetable = TimeTable.objects.all()
        form = CourseForm()
        return render(request, self.template_name, {'courses': courses, 'timetable':timetable, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TimeTableForm(request.POST)
        course_list = Course.objects.values_list(
                        'department', flat=True
                    ).distinct()
        
        group_by_department = {}
        group_list = []
        for value in course_list:
            group_by_department[value] = Course.objects.filter(department=value)
            group_list.append(Course.objects.filter(department=value))
    
        exam_date = request.POST.get('exam_date')
        
        exam_time = ["08:00:00", "11:00:00", "14:00:00"]
        count = 1
        TimeTable.objects.all().delete()
        for department in zip_longest(*group_by_department.values()):
            for course in department:
                if datetime.strptime(exam_date, "%Y-%m-%d").date().weekday() < 6:
                    randomly_selected_time = random.choice(exam_time)
                    if course is None:
                        continue
                    TimeTable.objects.create(course=course, exam_date=exam_date, exam_time=randomly_selected_time)
                if (count % 3 == 0):
                    exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
                    exam_date = str(exam_date + timedelta(days=1))
                count += 1            
        timetable = TimeTable.objects.all()
        context = {'timetable': timetable, 'form':form}
        return render(request, self.template_name, context)    
    
    
class SeatView(View):
    template_name = 'main/seats.html'

    def get(self, request, *args, **kwargs):
        seats = Seat.objects.all()
        form = SeatForm()
        context = {'seats': seats, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SeatForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:seats')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:seats')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Seat.objects.create(
                hall=row['hall'],
                student=row['student'],
                position_x=row['position_x'],
                position_y=row['position_y']
            )


class HallCreateView(AdminRequiredMixin, View):
    template_name = 'main/halls.html'

    def get(self, request, *args, **kwargs):
        halls = Hall.objects.all()
        form = HallForm()
        return render(request, self.template_name, {'halls': halls, 'form': form})

    def post(self, request, *args, **kwargs):
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:halls')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            hall = Hall.objects.create(
                name=row['name'],
                capacity=row['capacity'],
                description=row['description'],
                num_columns=row['num_columns'],
                num_rows=row['num_rows']
            )
            # Add courses and invigilators if needed
            # Example: hall.courses.add(course1, course2)
            # Example: hall.invigilators.add(invigilator1, invigilator2)

    def post(self, request, *args, **kwargs):
        form = HallForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:halls')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:halls')

        return render(request, self.template_name, {'form': form})
    

class TimeTableCreateView(AdminRequiredMixin, View):
    template_name = 'main/timetables.html'

    def get(self, request, *args, **kwargs):
        timetable = TimeTable.objects.all()
        form = TimeTableForm()
        return render(request, self.template_name, {'timetable': timetable, 'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            #exam_dat
            TimeTable.objects.create(
                course_id=row['course_id'],
                exam_date=row['exam_date'],
                exam_time=row['exam_time']
            )

    def post(self, request, *args, **kwargs):
        form = TimeTableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:timetables')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:timetables')

        return render(request, self.template_name, {'form': form})


class StudentSeatView(LoginRequiredMixin, TemplateView):
    template_name = 'main/student_seat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = None
        student_courses = None
        assigned_seat = None

        # if self.request.user.is_authenticated and isinstance(self.request.user, Student):
        if self.request.user.is_authenticated and self.request.user.user_type == "Student":
            student = get_object_or_404(Student, id=self.request.user.id)
            student_courses = student.get_courses()
            student_today_courses = student.get_today_courses()
            assigned_seat = Seat.objects.filter(student=student).first()
        context['student'] = student
        context['student_courses'] = student_courses
        context['student_today_courses'] = student_today_courses
        context['assigned_seat'] = assigned_seat

        return context