# utils.py
from django.utils import timezone
from .models import TimeTable


def get_today_courses():
    today_date = timezone.now().date()

    today_timetable_entries = TimeTable.objects.filter(exam_date=today_date)

    courses_today = [timetable_entry.course for timetable_entry in today_timetable_entries]
    return courses_today


def list_to_dict(lst):
    result_dict = {}
    for index, value in enumerate(lst):
        result_dict[index] = value
    return result_dict
    