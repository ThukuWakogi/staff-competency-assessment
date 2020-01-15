from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import User, Assessment_period, Assessment, Rating, Assessment_results, Competency, Strand
from .serializers import UserSerializer, PeriodSerializer, AssessmentSerializer,RatingSerializer,ResultsSerializer,CompetencySerializer, StrandSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed and edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)

        return Response(
            {
                'token': token.key,
                'user': serializer.data,
                'created': created
            },
            status = status.HTTP_201_CREATED,
            headers = headers
        )


class ObtainAuthTokenAndUserDetails(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(ObtainAuthTokenAndUserDetails, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)

        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'last_login': user.last_login,
                'is_superuser': user.is_superuser,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'date_joined': user.date_joined,
                'email': user.email,
                'level': user.level
            }
        })


class UserDetailsFromToken(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(
            user={
                'id': request.user.id,
                'last_login': request.user.last_login,
                'is_superuser': request.user.is_superuser,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
                'date_joined': request.user.date_joined,
                'email': request.user.email,
                'level': request.user.level
            }
        ))

class AssessmentPeriodViewSet(viewsets.ModelViewSet):
    queryset = Assessment_period.objects.all()
    serializer_class = PeriodSerializer

    # def list(self, request, *args, **kwargs):
    #     assessments_periods = Assessment_period.objects.all()
    #     serializer = PeriodSerializer(assessments_periods, many=True)

    #     return Response(serializer.data)
    def get_period(self,pk):
        try:
            return AssessmentPeriod.objects.get(pk=pk)
        except AssessmentPeriod.DoesNotExist:
            return Http404 

    def get(self, request, pk, format=None):
        period = self.get_period(pk)
        serializers = PeriodSerializer(period) 
        return Response(serializer.data)        

    def put(self, request, pk, format=None):
        period = self.get_period(pk)
        serializers = PeriodSerializer(period,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        period = self.get_period(pk)  
        period.delete()   
        return Response (status=status.HTTP_204_NO_CONTENT)


class AssessmentViewSet(viewsets.ModelViewSet):
        queryset = Assessment.objects.all()
        serializer_class = AssessmentSerializer

class  RatingViewSet(viewsets.ModelViewSet):
       queryset = Rating.objects.all()
       serializer_class = RatingSerializer

class AssessmentResultViewSet(viewsets.ModelViewSet):
       queryset = Assessment_results.objects.all()
       serializer_class = ResultsSerializer

class CompetencyViewSet(viewsets.ModelViewSet):
       queryset = Competency.objects.all()
       serializer_class = CompetencySerializer  

class StrandViewSet(viewsets.ModelViewSet):
      queryset = Strand.objects.all()
      serializer_class = StrandSerializer          
