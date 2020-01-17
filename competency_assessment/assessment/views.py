from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
import json

from .models import User, Assessment_period, Team, TeamLeader
from .serializers import UserSerializer, PeriodSerializer, TeamSerializer

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


class TeamViewSet(APIView):
    # queryset = Team.objects.all()
    # serializer_class = TeamSerializer

    def get(self, request, format=None):
        managers = TeamLeader.objects.all()
        managers_emails = set()
        users_by_managers = {}

        for manager in managers:
            #print(manager.manager)
            managers_emails.add(manager.user)

        for email in managers_emails:
            manager = User.objects.get(email=email)
            print(manager)
            
            # staff_email = Team.objects.filter(users_in_team=manager)

            # for staff in staff_email:
            #     print('    ' + str(staff.user_id))
            #     user = User.objects.get(email=staff)
            #     print(user.__dict__)

        # # users_by_managers = dict.keys('manager', 'staff_under_manager')
        # users_by_managers['manager'] = manager
        # users_by_managers['staff'] = staff.user_id

        # print(users_by_managers)

        return Response({'lol': 'lol'})



# class DirectManagerViewSet(viewsets.ModelViewSet):
#     queryset = Direct_manager.objects.all()
#     serializer_class = DirectManagerSerializer

#     def list(self, request, *args, **kwargs):
#         managers = Direct_manager.objects.all()
#         serializer = DirectManagerSerializer(managers, many=True)
#         managers_expanded = []

#         for manager in serializer.data:
#             staff = User.objects.get(id=dict(manager)['staff'])
#             managers_expanded.append({
#                 'id': dict(manager)['id'],
#                 'name': dict(manager)['name'],
#                 'staff': {
#                     'id': staff.id,
#                   manager  'last_login': staff.last_login,
#                     'is_superuser': staff.is_superuser,
#                     'first_name': staff.first_name,
#                     'last_name': staff.last_name,
#                     'is_staff': staff.is_staff,
#                     'date_joined': staff.date_joined,
#                     'email': staff.email,

#                 }
#             })

#         return Response(managers_expanded)

#**********************************************************************8

# class UsersByManagers(APIView):
#     def get(self, request, format=None):
#         managers = Direct_manager.objects.all()
#         managers_emails = set()
#         users_by_managers = {}

#         for manager in managers:
#             #print(manager.manager)
#             managers_emails.add(manager.manager)

#         for email in managers_emails:
#             manager = User.objects.get(email=email)
#             print(manager)
#             staff_email = Direct_manager.objects.filter(manager=manager)

#             for staff in staff_email:
#                 print('    ' + str(staff.user_id))
#             #     user = User.objects.get(email=staff)
#             #     print(user.__dict__)

#         # users_by_managers = dict.keys('manager', 'staff_under_manager')
#         users_by_managers['manager'] = manager
#         users_by_managers['staff'] = staff.user_id

#         print(users_by_managers)

#         return Response({'lol': 'lol'})