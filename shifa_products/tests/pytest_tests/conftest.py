from django.urls import reverse
import pytest


@pytest.fixture
def index_url():
    return reverse(
        'pages:index'
    )
