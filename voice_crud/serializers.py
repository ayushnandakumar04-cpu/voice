from rest_framework import serializers
from voice_crud.models import Feedback
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["username","email","password"]


class FeedBackSerializers(serializers.ModelSerializer):

    class Meta:

        model=Feedback

        fields="__all__"

        read_only_fields=["id","student","sentiment","created_at"]

    def validate_department(self, value):
        allowed_departments = [
            'CSE', 'ECE', 'EEE', 'ME', 'CE', 'IT'
        ]

        if value.upper() not in allowed_departments:
            raise serializers.ValidationError(
                "Invalid department."
            )

        return value.upper()

    def validate_feedback_text(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Feedback must contain at least 10 characters."
            )

        return value.strip()
