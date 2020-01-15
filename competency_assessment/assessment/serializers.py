from rest_framework import serializers
from .models import User, Assessment_period, Direct_manager

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
        model = Assessment_period
        fields = ('id', 'start_date', 'end_date', 'initiating_user') 


class DirectManagerSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Direct_manager
        fields = ('user_id', 'manager')