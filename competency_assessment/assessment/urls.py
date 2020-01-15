from django.urls import path, include
from rest_framework import routers
from competency_assessment.assessment import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet),
router.register(r'assessment-period', views.AssessmentPeriodViewSet),
router.register(r'assessments', views.AssessmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.ObtainAuthTokenAndUserDetails.as_view()),
    path('udft/', views.UserDetailsFromToken.as_view())
]