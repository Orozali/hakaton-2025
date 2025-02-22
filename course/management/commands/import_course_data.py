import json
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from course.models import Course
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'  # Замените на путь к вашим настройкам
django.setup()

class Command(BaseCommand):
    help = 'Import course data from JSON file'

    def handle(self, *args, **kwargs):
        # Чтение данных из JSON файла
        try:
            with open("course/formatted_data_updated.json", "r", encoding="utf-8") as file:
                formatted_data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("The file formatted_data_updated.json was not found."))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Failed to decode JSON file."))
            return

        for data in formatted_data:
            winter_date = None
            summer_date = None

            # Обработка даты для зимнего семестра
            if data['deadlines'].get('winter'):
                try:
                    date_string = re.sub(r"\(.*\)", "", data['deadlines']['winter']).strip()
                    winter_date = datetime.strptime(date_string, "%d %B").replace(year=2025)
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Invalid winter date format for course {data['id']}: {e}"))
                    winter_date = None

            # Обработка даты для летнего семестра
            if data['deadlines'].get('summer'):
                try:
                    date_string = re.sub(r"\(.*\)", "", data['deadlines']['summer']).strip()
                    summer_date = datetime.strptime(date_string, "%d %B").replace(year=2025)
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Invalid summer date format for course {data['id']}: {e}"))
                    summer_date = None

            # Создание объекта Course в базе данных
            try:
                course = Course.objects.create(
                    course_id=data["id"],
                    has_grade_requirement=data["gpa"].get("has_grade_requirement", False),
                    original_grade=data["gpa"].get("original_grade", ""),
                    grade_system=data["gpa"].get("grade_system", ""),
                    qualitative_grade=data["gpa"].get("qualitative_grade", ""),
                    is_gre_required=data["gre"].get("is_gre_required", False),
                    gre_score_required=data["gre"].get("gre_score_required", 0),
                    is_gre_optional=data["gre"].get("is_gre_optional", False),
                    is_joint_degree=data.get("is_joint_degree", False),
                    is_combined_degree=data.get("is_combined_degree", False),
                    winter_date=winter_date,
                    summer_date=summer_date,
                    ielts=data["language"].get("ielts", 0),
                    toefl_ibt=data["language"].get("toefl_ibt", 0),
                    toefl_pbt=data["language"].get("toefl_pbt", 0),
                    cerf=data["language"].get("cefr", ""),
                )
                self.stdout.write(self.style.SUCCESS(f"Course {course.course_id} created successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating course {data['id']}: {e}"))
