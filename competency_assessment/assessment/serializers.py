from rest_framework import serializers
from .models import User, AssessmentPeriod, Rating, Competency, Strand, Assessment, AssessmentResults, Idp, Notification,JobGrade


# Create your views here.
# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = dict(
            password={
                'write_only': True,
                'required': True,
                'allow_null': False
            },
            email={
                'required': True,
                'allow_null': False
            },
            first_name={
                'required': True,
                'allow_null': False
            },
            last_name={
                'required': True,
                'allow_null': False
            }
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPeriod
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = ('name')


class StrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Strand
        fields = ('name', 'competency')


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'


class AssessmentResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResults
        fields = '__all__'


class IdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class AssessmentPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPeriod
        fields = '__all__'

class JobGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobGrade
        fields = '__all__'