from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from datetime import datetime

from .models import *
from .serializers import UserSerializer, PeriodSerializer, AssessmentSerializer, RatingSerializer, ResultsSerializer, \
    CompetencySerializer, IdpSerializer, StrandSerializer, NotificationSerializer, AssessmentPeriodSerializer


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
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ObtainAuthTokenAndUserDetails(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(ObtainAuthTokenAndUserDetails, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)

        return Response({
            'token': token.key,
            'user': {
                **UserSerializer(user).data,
                'is_manager':
                    False
                    if len([manager.user_id for manager in DirectManager.objects.filter(manager=user)]) == 0 else True
            }
        })


class UserDetailsFromToken(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(
            user={
                **UserSerializer(request.user).data,
                'is_manager':
                    False
                    if len([manager.user_id for manager in DirectManager.objects.filter(manager=request.user)]) == 0
                    else True
            }
        ))


class AssessmentPeriodViewSet(viewsets.ModelViewSet):
    queryset = AssessmentPeriod.objects.all()
    serializer_class = PeriodSerializer

    def get_period(self, pk):
        try:
            return AssessmentPeriod.objects.get(pk=pk)
        except AssessmentPeriod.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        period = self.get_period(pk)
        serializer = PeriodSerializer(period)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        period = self.get_period(pk)
        serializers = PeriodSerializer(period, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        period = self.get_period(pk)
        period.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.get(email=request.data['user_email'])
        assessment_period = AssessmentPeriod.objects.get(pk=request.data['assessment_period'])
        assessment = Assessment.objects.create(user_id=user, assessment_period=assessment_period)
        results = []

        for result in request.data['results']:
            competency = Competency.objects.get(pk=result['competency']['id'])
            for strand in result['competency']['strands']:
                _strand = Strand.objects.get(pk=strand['id'])
                rating = Rating.objects.get(pk=strand['rating_id'])
                results.append(
                    AssessmentResults(
                        assessment=assessment,
                        user_id=user,
                        competency=competency,
                        strand=_strand,
                        rating=rating
                    )
                )

        AssessmentResults.objects.bulk_create(results)
        posted_results = {
            'user_email': user.email,
            'assessment_period': assessment_period.id,
            'assessment_id': assessment.id
        }

        return Response(posted_results)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class AssessmentResultViewSet(viewsets.ModelViewSet):
    queryset = AssessmentResults.objects.all()
    serializer_class = ResultsSerializer


class CompetencyViewSet(viewsets.ModelViewSet):
    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer


class StrandViewSet(viewsets.ModelViewSet):
    queryset = Strand.objects.all()
    serializer_class = StrandSerializer


class IdpViewSet(viewsets.ModelViewSet):
    queryset = Idp.objects.all()
    serializer_class = IdpSerializer


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UsersByManager(ViewSet):
    queryset = DirectManager.objects.all()

    def list(self, request):
        managers = set()
        users_by_manager = []

        for result in self.queryset:
            managers.add(result.manager)

        for manager in managers:
            users = []

            for staff in self.queryset:
                if staff.manager.email == manager.email:
                    users.append({**UserSerializer(staff.user_id).data})

            users_by_manager.append({
                "manager": {
                    **UserSerializer(manager).data,
                    "staff": users
                }
            })

        return Response(users_by_manager)


class AssessmentPeriodSummary(ViewSet):
    queryset = AssessmentPeriod.objects.all()

    def list(self, request):
        return Response({
            'total_assessment_periods': len(self.queryset),
            'previous_assessment_period': {
                **AssessmentPeriodSerializer(self.queryset.last()).data,
                'has_ended': datetime(
                    self.queryset.last().end_date.year,
                    self.queryset.last().end_date.month,
                    self.queryset.last().end_date.day
                ) < datetime.now()
            },
        })
