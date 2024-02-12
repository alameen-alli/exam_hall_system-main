from django.contrib import admin
from .models import (Faculty, Department, Course, 
                     Offer, TimeTable, Seat, Hall)

# Register your models here.
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Offer)
admin.site.register(TimeTable)
admin.site.register(Seat)
admin.site.register(Hall)


