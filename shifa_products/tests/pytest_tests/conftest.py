from django.urls import reverse
import pytest

from catalog.models import Category


@pytest.fixture
def index_url():
    return reverse(
        'pages:index'
    )


@pytest.fixture
def about_us_url():
    return reverse(
        'pages:about_us'
    )


@pytest.fixture
def category_url():
    return reverse(
        'catalog:category_list'
    )


@pytest.fixture
def create_category():
    return Category.objects.create(
        name='Category 1', slug='category-1'
    )


@pytest.fixture
def category_product_list_url(create_category):
    return reverse(
        'catalog:category_product_list',
        args=(create_category.slug,)
    )
