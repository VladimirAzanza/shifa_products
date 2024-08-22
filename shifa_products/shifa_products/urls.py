from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm

auth_urls = [
    path('', include('django.contrib.auth.urls')),
    path(
        'registration/',
        CreateView.as_view(
            template_name='registration/signup.html',
            form_class=UserForm,
            success_url=reverse_lazy('pages:index'),
        ),
        name='registration'
    )
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('', include('pages.urls', namespace='pages')),
    path('users/', include('users.urls', namespace='users'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
