from rest_framework import serializers
from .models import User, Assessment_period, Rating, Competency, Strand, Assessment, Assessment_results

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
    #initiating_user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Assessment_period
        fields = '__all__'     
2

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('name', 'rating')   

class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Competency
        fields = ('name')  

class StrandSerializer(serializers.ModelSerializer):
    competency = CompetencySerializer(many=True, read_only=True)
    class Meta:
        model = Strand
        fields = ('name', 'competency')  

class AssessmentSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(many=True, read_only=True)
    assessment_period = PeriodSerializer(many=True, read_only=True)
    class Meta:
        model = Assessment 
        fields = ('user_id','assessment_period', 'is_assessed_by_manager', 'is_assessed_after_norming')

class ResultsSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(many=True, read_only=True)
    assessment = AssessmentSerializer(many=True, read_only=True)
    strand = StrandSerializer(many=True,read_only=True)
    rating = RatingSerializer(many=True,read_only=True)
    class Meta:
        model = Assessment_results
        fields = ('user_id', 'assessment', 'competency', 'strand', 'rating')
