from django.urls import path, include
from rest_framework import routers
from competency_assessment.assessment import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet),
router.register(r'assessment-period', views.AssessmentPeriodViewSet),
router.register(r'assessments', views.AssessmentViewSet),
router.register(r'ratings', views.RatingViewSet),
router.register(r'assessment-results', views.AssessmentResultViewSet),
router.register(r'competencies',views.CompetencyViewSet),
router.register(r'strands', views.StrandViewSet),
router.register(r'idps', views.IdpViewSet),
router.register(r'notifications', views.NotificationsViewSet)
router.register(r'managers/users', views.UsersByManager, basename='usersbymanager')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.ObtainAuthTokenAndUserDetails.as_view()),
    path('udft/', views.UserDetailsFromToken.as_view()),
    path('usersbymanager/', views.TeamViewSet.as_view()),
    # path('managers/users/', views.UsersByManager.as_view({'get': 'list'}))
]