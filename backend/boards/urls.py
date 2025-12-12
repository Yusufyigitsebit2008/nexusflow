from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkspaceViewSet, BoardViewSet, ListViewSet, CardViewSet,CommentViewSet,RegisterView,GenerateDemoDataView,GlobalSearchView,AttachmentViewSet,ChecklistItemViewSet
from .views import ActivityViewSet

router = DefaultRouter()
router.register(r'workspaces', WorkspaceViewSet, basename='workspace')
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'lists', ListViewSet)
router.register(r'cards', CardViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'attachments', AttachmentViewSet),
router.register(r'checklists', ChecklistItemViewSet)
router.register(r'activities', ActivityViewSet, basename='activity')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('generate-demo/', GenerateDemoDataView.as_view(), name='generate-demo'),
    path('search/', GlobalSearchView.as_view(), name='global-search'),
]