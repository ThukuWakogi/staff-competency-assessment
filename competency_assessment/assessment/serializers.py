from rest_framework import serializers
from .models import User

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