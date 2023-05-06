from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken import views
from rest_framework_nested import routers
from api.view.comment_view import CommentViewSet
from api.view.lecture_view import LectureViewSet
from api.view.proposal_view import ProposalViewSet
from api.view.user_view import UserViewSet
from api.view.favorite_view import FavoriteViewSet
from api.view.lecture_customer_view import LectureCustomerViewSet

router = routers.DefaultRouter()

""" Comment """
router.register(r"comments", CommentViewSet)

""" Lecture """
router.register(r"lectures", LectureViewSet)

""" Proposal """
router.register(r"proposals", ProposalViewSet)

""" User """
router.register(r"users", UserViewSet)

""" Favorite """
router.register(r"favorites", FavoriteViewSet)

""" LectureCustomer """
router.register(r"lecture_customers", LectureCustomerViewSet)

# Basic router
urlpatterns = router.urls

urlpatterns += [path("authorizations/", views.obtain_auth_token)]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
