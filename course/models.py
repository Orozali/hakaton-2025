from django.db import models


class Course(models.Model):
    course_location = models.CharField(max_length=255, blank=True, null=True)
    in_cooperation_with = models.TextField(blank=True, null=True)
    teaching_language = models.CharField(max_length=100, blank=True, null=True)
    language_level_of_course = models.TextField(blank=True, null=True)
    date_info = models.TextField(blank=True, null=True)
    target_group = models.TextField(blank=True, null=True)
    description_content = models.TextField(blank=True, null=True)
    recognised_language_exams = models.CharField(max_length=255, blank=True, null=True)
    other_degrees_awarded = models.CharField(max_length=255, blank=True, null=True)
    ects_points = models.IntegerField(blank=True, null=True)
    avg_hours_per_week = models.IntegerField(blank=True, null=True)
    avg_participants_per_group = models.IntegerField(blank=True, null=True)
    dates_and_costs = models.TextField(blank=True, null=True)
    price_includes = models.TextField(blank=True, null=True)
    funding_info = models.TextField(blank=True, null=True)
    language_requirements = models.TextField(blank=True, null=True)
    submit_application_to = models.TextField(blank=True, null=True)
    accommodation_organised = models.BooleanField(default=False)
    type_of_accommodation = models.TextField(blank=True, null=True)
    meals = models.TextField(blank=True, null=True)
    social_and_leisure_programme_offered = models.BooleanField(default=False)
    social_and_leisure_programme_description = models.TextField(blank=True, null=True)
    free_internet_access = models.BooleanField(default=False)
    support_in_visa_matters = models.BooleanField(default=False)
    pick_up_service = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    university_name = models.CharField(max_length=255, blank=True, null=True)
    university_description = models.TextField(blank=True, null=True)
    university_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.university_name or "Course"
