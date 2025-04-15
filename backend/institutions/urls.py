from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InstitutionViewSet, InstitutionGenerateCodeAPIView,
    InstitutionJoinAPIView, InstitutionMemberAPIView,
    InstitutionJoinRequestAPIView
)

router = DefaultRouter()
router.register(r'', InstitutionViewSet, basename="institution")
# router.register(r'join-requests', InstitutionJoinRequestViewSet)

urlpatterns = [
    path('join/', InstitutionJoinAPIView.as_view()), 
    path('<str:institution_id>/generate-code/', InstitutionGenerateCodeAPIView.as_view()),
    path('<str:institution_id>/members/', InstitutionMemberAPIView.as_view()),
    path('<str:institution_id>/members/<str:user_id>/', InstitutionMemberAPIView.as_view()),
    path('<str:institution_id>/join-requests/', InstitutionJoinRequestAPIView.as_view()),
    path('<str:institution_id>/join-requests/<str:request_id>/', InstitutionJoinRequestAPIView.as_view()),
    path('', include(router.urls)),
    # path('institutions/join', JoinInstitutionViewSet.as_view({'post': 'join'}), name='join-institution'),
] 