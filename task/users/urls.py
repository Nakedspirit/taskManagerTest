from django.conf.urls import url

from rest_framework.authtoken import views as rest_views

from . import views


urlpatterns = [
    url(
        r'^api-token-auth/',
        rest_views.obtain_auth_token
    ),

    url(
        r'^reports/$',
        views.UserReports.as_view(),
        name='user-reports'
    ),

    url(
        r'^users/$',
        views.UserCreate.as_view(),
        name='user-create'
    ),

    url(
        r'^users/(?P<pk>\d+)/$',
        views.UserDetail.as_view(),
        name='user-detail'
    ),

    url(
        r'^users/(?P<pk>\d+)/filterrole/$',
        views.UserViewSetRole.as_view(),
        name='task-filter-role'
    ),

    url(
        r'^users/(?P<pk>\d+)/filtertask/$',
        views.UserViewSetAssignee.as_view(),
        name='task-filter-task'
    ),

]
