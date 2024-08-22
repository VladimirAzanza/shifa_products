from django.urls import path
from django.views.generic import TemplateView


app_name = 'pages'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='pages/index.html'),
        name='index'
    ),
    path(
        'about_us',
        TemplateView.as_view(template_name='pages/contact.html'),
        name='about_us'
    ),
]
