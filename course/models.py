from django.db import models


class Course(models.Model):
    course_id = models.IntegerField()

    has_grade_requirement = models.BooleanField(default=False)
    original_grade = models.FloatField(blank=True, null=True)
    grade_system = models.CharField(max_length=20, blank=True, null=True)
    qualitative_grade = models.CharField(max_length=10, blank=True, null=True)

    is_gre_required = models.BooleanField(default=False)
    gre_score_required = models.FloatField(blank=True, null=True)
    is_gre_optional = models.BooleanField(default=False)

    is_joint_degree = models.BooleanField(default=False)
    is_combined_degree = models.BooleanField(default=False)

    winter_date = models.DateField(blank=True, null=True)
    summer_date = models.DateField(blank=True, null=True)

    ielts = models.FloatField(blank=True, null=True)
    toefl_ibt = models.FloatField(blank=True, null=True)
    toefl_pbt = models.FloatField(blank=True, null=True)
    cerf = models.CharField(max_length=10, blank=True, null=True)
    uni_assist = models.BooleanField(default=False)
