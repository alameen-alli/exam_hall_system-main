# main/management/commands/populate_sample_data.py
from itertools import zip_longest
from django.core.management.base import BaseCommand
from main.models import Faculty, Department, Course, Offer, Hall, Seat, TimeTable
from accounts.models import Student, Invigilator
from django.utils import timezone
import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample faculties
        faculty1 = Faculty.objects.create(name='Arts and Humanities')
        faculty2 = Faculty.objects.create(name='Science')
        faculty3 = Faculty.objects.create(name='Social Sciences')
        
        department1 = Department.objects.create(name='Literature', faculty=faculty1)
        department2 = Department.objects.create(name='Physics', faculty=faculty2)
        department3 = Department.objects.create(name='Sociology', faculty=faculty3)
        department4 = Department.objects.create(name='Chemistry', faculty=faculty2)
        department5 = Department.objects.create(name='Mathematics', faculty=faculty2)
        self.stdout.write(self.style.SUCCESS('Departments created successfully'))
        
        # Create sample courses
        course1 = Course.objects.create(name='Introduction to Literary Analysis', code='LIT101', department= department1)
        course2 = Course.objects.create(name='American Literature Survey', code='LIT201', department= department1)
        course3 = Course.objects.create(name='British Romantic Poetry', code='LIT301', department= department1)
        course4 = Course.objects.create(name='Contemporary World Fiction', code='LIT401', department= department1)
        course5 = Course.objects.create(name='Shakespearean Tragedies', code='LIT501', department= department1)
        
        course6 = Course.objects.create(name='Classical Mechanics', code='PHY101', department=department2)
        course7 = Course.objects.create(name='Quantum Mechanics', code='PHY201', department=department2)
        course8 = Course.objects.create(name='Electromagnetism', code='PHY301', department=department2)
        course9 = Course.objects.create(name='Thermodynamics and Statistical Mechanics', code='PHY401', department=department2)
        course10 = Course.objects.create(name='Astrophysics', code='PHY501', department=department2)
        
        course11 = Course.objects.create(name='General Chemistry', code='CHEM101', department=department4)
        course12 = Course.objects.create(name='Organic Chemistry', code='CHEM201', department=department4)
        course13 = Course.objects.create(name='Inorganic Chemistry', code='CHEM301', department=department4)
        course14 = Course.objects.create(name='Physical Chemistry', code='CHEM401', department=department4)
        course15 = Course.objects.create(name='Analytical Chemistry', code='CHEM501', department=department4)
        
        course16 = Course.objects.create(name='Calculus I', code='MATH101', department=department5)
        course17 = Course.objects.create(name='Linear Algebra', code='MATH201', department=department5)
        course18 = Course.objects.create(name='Differential Equations', code='MATH301', department=department5)
        course19 = Course.objects.create(name='Abstract Algebra', code='MATH401', department=department5)
        course20 = Course.objects.create(name='Real Analysis', code='MATH501', department=department5)
        
        course21 = Course.objects.create(name='Introduction to Sociology', code='SOC101', department=department3)
        course22 = Course.objects.create(name='Social Research Methods', code='SOC201', department=department3)
        course23 = Course.objects.create(name='Gender and Society', code='SOC301', department=department3)
        course24 = Course.objects.create(name='Sociology of Deviance', code='SOC401', department=department3)
        course25 = Course.objects.create(name='Contemporary Social Issues', code='SOC501', department=department3)
        self.stdout.write(self.style.SUCCESS('Courses created successfully'))
        
        departments_courses = {
            department1: [course1, course2, course3, course4, course5],
            department2: [course6, course7, course8, course9, course10],
            department3: [course21, course22, course23, course24, course25],
            department4: [course11, course12, course13, course14, course15],
            department5: [course16, course17, course18, course19, course20],
        }

        student_list = []
        for i in range(101, 501):
            username = f'student{i}'
            email = f'student{i}@example.com'
            password = make_password(username)  # Hash the username to set as the password
            student = Student.objects.create(username=username, email=email, password=password)
            student_list.append(student)
            self.stdout.write(self.style.SUCCESS(f'{student} created successfully'))
        self.stdout.write(self.style.SUCCESS('Students created successfully'))

                    
        courses = Course.objects.all()
        
        for i, student in enumerate(student_list):
            if i < 100:
                student.department = department1
            elif i < 200:
                student.department = department2
            elif i < 300:
                student.department = department3
            elif i < 400:
                student.department = department4
            else:
                student.department = department5

            # Assign random courses from the chosen department
            student_courses = random.sample(departments_courses[student.department], k=3)
            
            # Create Offer instances for each assigned course
            for course in student_courses:
                Offer.objects.create(student=student, course=course)
        self.stdout.write(self.style.SUCCESS('Students offering courses created successfully'))
        self.stdout.write(self.style.SUCCESS('Sample data populated successfully'))
