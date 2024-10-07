from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'profile/<slug:username>',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'profile/<slug:username>/update/',
        views.ProfileUpdateView.as_view(),
        name='profile_update'
    ),
    path(
        'profile/create_address/',
        views.AddressUserCreateView.as_view(),
        name='address_create'
    ),
    path(
        'profile/delete_address/<int:address_id>/',
        views.AddressUserDeleteView.as_view(),
        name='address_delete'
    ),

]
