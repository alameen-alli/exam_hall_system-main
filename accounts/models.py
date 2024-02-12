from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from main.utils import get_today_courses
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=20, verbose_name="User Type")
    slug = models.SlugField(unique=True, blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            Profile.objects.create(user=self)

    def __str__(self):
        return self.username + " " + self.email


class Student(CustomUser):
    LEVEL_CHOICES = (
        (100, '100'),
        (200, '200'),
        (300, '300'),
        (400, '400'),
    )
        
    level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        
    def __str__(self):
        # Get the courses the student is offering
        today_courses = get_today_courses()
        all_offers = self.offer.all()
        # Extract course IDs from today_courses and all_offers
        today_courses_ids = set(course.id for course in today_courses)
        all_offers_ids = set(offer.course.id for offer in all_offers)

        # Find common course IDs
        common_course_ids = today_courses_ids.intersection(all_offers_ids)

        # Filter offers for common courses
        student_offers = all_offers.filter(course__id__in=common_course_ids)
        # Extract the course names and join them into a comma-separated string
        course_names = ", ".join(str(offer.course).upper() for offer in student_offers)
        # return f"[{self.username}]"
        return f"[{self.username}] - Courses: {course_names}"
        
    def get_today_courses(self):
        today_courses = get_today_courses()
        courses_offered = self.get_courses()    
        print("All offers: ", courses_offered)
        print("Today courses: ", today_courses)
        # # Extract course IDs from today_courses and all_offers
        # today_courses_ids = set(course.id for course in today_courses)
        # all_offers_ids = set(offer.course.id for offer in all_offers)

        # # Find common course IDs
        # common_course_ids = today_courses_ids.intersection(all_offers_ids)

        # student_offers = all_offers.filter(course__id__in=common_course_ids)
        # courses = [offer.course for offer in student_offers]
        courses = [course for course in today_courses if course in courses_offered]
        print(courses)
        return courses
    
    def get_courses(self):
        courses_offered = []
        all_offers = self.offer.all()
        for offer in all_offers:
            courses_offered.append(offer.course)
        return courses_offered
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = False
            self.user_type = "Student"
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("accounts:student_profile", kwargs={"slug": self.slug})


class Invigilator(CustomUser):
    hall = models.ForeignKey('main.Hall', on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        verbose_name = 'Invigilator'
        verbose_name_plural = 'Invigilators'
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True
            self.user_type = "Invigilator"
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("accounts:invigilator_profile", kwargs={"slug": self.slug})
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
