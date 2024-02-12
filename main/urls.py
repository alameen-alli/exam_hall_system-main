# main/urls.py

from django.urls import path
from .views import (
    hall_seats_view,
    AllocateSeatsView,
    CourseCreateView,
    TimeTableCreateView,
    SeatView,
    HallCreateView,
    AdminDashboardView,
    GenerateTimeTableView,
    StudentSeatView,
)

app_name = "main"

urlpatterns = [
    path('allocated-student-seats/', hall_seats_view, name='allocated_seats'),
    path('generate-timetable/', GenerateTimeTableView.as_view(), name='generate'),
    path('allocate-seats/', AllocateSeatsView.as_view(), name='allocate'),
    path('courses/', CourseCreateView.as_view(), name='courses'),
    path('add-timetable/', TimeTableCreateView.as_view(), name='create_timetable'),
    path('seats-view/', SeatView.as_view(), name='seats'),
    path('halls/', HallCreateView.as_view(), name='halls'),
    path('timetables/', TimeTableCreateView.as_view(), name='timetables'),
    path('allotments/', HallCreateView.as_view(), name='allotments'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('student-seat/', StudentSeatView.as_view(), name='student_seat'),
    # path('timetable/<int:timetable_id>/', views.timetable_detail, name='timetable_detail'),
]
