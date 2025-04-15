from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views.auth_views import CustomLoginView
from core.views.auth_views import OrganizerRegisterView
from core.views.event_viewset import EventViewSet


from core.views.organization import JoinOrganizationView, OrganizationMembersView, remove_member

from .views import (
    RegisterView,
    BGGSearchView,
    GameListView,
    UserCollectionView,
    AddToCollectionView,
    OrganizationViewSet,
    GameCategoryViewSet,
)

urlpatterns = [

    # 🔐 Autentifikacija
    path('register/', RegisterView.as_view(), name='register'),

    # 🎲 Žaidimai
    path('games/', GameListView.as_view(), name='game-list'),

    # 📚 Kolekcija
    path('collection/', UserCollectionView.as_view(), name='user-collection'),
    path('collection/add/', AddToCollectionView.as_view(), name='add-to-collection'),

    # 🔍 Paieška iš BGG
    path('bgg/search/', BGGSearchView.as_view(), name='bgg-search'),

    path('organizations/<int:pk>/join/', JoinOrganizationView.as_view(), name='join-organization'),
    path('organizations/<int:pk>/members/', OrganizationMembersView.as_view(), name='organization-members'),
    path('organizations/<int:org_id>/members/<int:user_id>/remove/', remove_member, name='remove-member'),
    path('token/', CustomLoginView.as_view(), name='custom-token'),
    path('register/organizer/', OrganizerRegisterView.as_view(), name='organizer-register'),
]

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'categories', GameCategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')

urlpatterns += router.urls
