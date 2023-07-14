from django.forms import ValidationError
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, data):
        # print(Course.objects.get(id=1).students.count())
            if Course.objects.get(name='test1').students.count() > 10:
                raise ValidationError('Превышено количество студентов, макс = 20')
            return data