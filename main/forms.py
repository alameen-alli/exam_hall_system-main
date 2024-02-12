# forms.py

from django import forms
from .models import Course, Offer, TimeTable, Seat, Hall
from accounts.models import CustomUser


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'department']
        
        
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['student', 'course']


class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['course', 'exam_date', 'exam_time']


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['hall', 'student', 'position_x', 'position_y']


class HallForm(forms.ModelForm):
    invigilators = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Hall
        fields = ['name', 'capacity', 'description', 'courses', 
                  'num_columns', 'num_rows', 'invigilators']

    def __init__(self, *args, **kwargs):
        super(HallForm, self).__init__(*args, **kwargs)
        # Customize the form if needed, for example, you can set a custom label
        self.fields['name'].label = 'Hall Name'


