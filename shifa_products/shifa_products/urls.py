from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

from .telegram_notifications import tawkto_webhook
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
    path('', include('pages.urls', namespace='pages')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('users/', include('users.urls', namespace='users')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('orders.urls', namespace='orders')),
    path('webhook/tawkto/', tawkto_webhook, name='tawkto_webhook'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
