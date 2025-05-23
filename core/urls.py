from django.urls import path
from rest_framework.routers import DefaultRouter
from core.views.auth_views import CustomLoginView
from core.views.auth_views import OrganizerRegisterView
from core.views.event_viewset import EventViewSet
from core.views.game_collection_viewset import GameCollectionViewSet
from rest_framework.routers import DefaultRouter


from core.views.organization import OrganizationMembersView, remove_member

from .views import (
    RegisterView,
    BGGSearchView,
    GameListView,
    UserCollectionView,
    AddToCollectionView,
    OrganizationViewSet,
    GameCategoryViewSet,
)
from .views.bgg_views import ImportGameByBGGId
from .views.event_game_import_view import EventGameImportView, EventAvailableGameListView
from .views.event_grouped_list_view import GroupedEventsView
from .views.event_importable_games_view import EventImportableGamesView
from .views.event_manage import MakeOrganizerView, KickPlayerView, RemoveOrganizerView
from .views.event_vote_view import EventGameVoteView, EventGameVoteResultsView
from .views.game_collection_bgg_import import AddGameFromSearchView
from .views.game_collection_csv_import import GameCollectionCSVImportView
from .views.game_collection_delete import RemoveGameFromCollectionView
from .views.organization_views import UserOrganizationsView
from .views.stats_view import StatsView
from .views.user_profile_view import UserFullProfileView
from .views.user_search import UserSearchView
from .views.user_views import CurrentUserView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('games/', GameListView.as_view(), name='game-list'),
    path('collection/', UserCollectionView.as_view(), name='user-collection'),
    path('collection/add/', AddToCollectionView.as_view(), name='add-to-collection'),
    path('users/search/', UserSearchView.as_view(), name="user-search"),
    path('bgg/search/', BGGSearchView.as_view(), name='bgg-search'),

    path('organizations/<int:pk>/members/', OrganizationMembersView.as_view(), name='organization-members'),
    path('organizations/<int:org_id>/members/<int:user_id>/remove/', remove_member, name='remove-member'),
    path('token/', CustomLoginView.as_view(), name='custom-token'),
    path('register/organizer/', OrganizerRegisterView.as_view(), name='organizer-register'),
    path('organizations/user/', UserOrganizationsView.as_view(), name='user-organizations'),
    path("collections/import-csv/", GameCollectionCSVImportView.as_view(), name="collection-import-csv"),
    path("collections/import-bgg-id/", ImportGameByBGGId.as_view(), name="import-bgg-id"),
    path('bgg/search/', BGGSearchView.as_view(), name='bgg-search'),
    path('bgg/import/', ImportGameByBGGId.as_view(), name='bgg-import'),
    path('collections/add-from-search/', AddGameFromSearchView.as_view(), name='add-from-search'),
    path('collections/<int:game_id>/delete/', RemoveGameFromCollectionView.as_view(), name='collection-delete'),
    path('events/<int:pk>/make-organizer/', MakeOrganizerView.as_view(), name='make-organizer'),
    path('events/<int:pk>/kick-player/', KickPlayerView.as_view(), name='kick-player'),
    path('events/<int:pk>/remove-organizer/', RemoveOrganizerView.as_view(), name='remove-organizer'),
    path('events/<int:pk>/import-games/', EventGameImportView.as_view(), name='import-games'),
    path('events/<int:pk>/available-games/', EventAvailableGameListView.as_view(), name='available-games'),
    path('events/<int:pk>/vote/', EventGameVoteView.as_view(), name='event-vote'),
    path('events/<int:pk>/vote-results/', EventGameVoteResultsView.as_view(), name='event-vote-results'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('organizations/<int:org_id>/remove-member/<int:user_id>/', remove_member, name='remove-member'),
    path('events/<int:pk>/importable-games/', EventImportableGamesView.as_view()),
    path('organizations/<int:org_id>/grouped-events/', GroupedEventsView.as_view(), name='grouped-events'),
    path('events/grouped/', GroupedEventsView.as_view(), name='grouped-events'),
    path('events/grouped/<int:org_id>/', GroupedEventsView.as_view(), name='grouped-events-by-org'),
    path('stats/', StatsView.as_view(), name='stats'),

    path('users/me/full/', UserFullProfileView.as_view(), name='user-full-profile'),


]

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'categories', GameCategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')
router.register(r'collections', GameCollectionViewSet, basename='collections')
urlpatterns += router.urls
