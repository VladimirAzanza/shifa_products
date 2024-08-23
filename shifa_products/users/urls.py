from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'profile/<slug:username>',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
]
