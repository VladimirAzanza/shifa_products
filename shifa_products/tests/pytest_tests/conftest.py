from django.urls import reverse
import pytest

from catalog.models import Category, Location, Product


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


@pytest.fixture
def create_location():
    return Location.objects.create(name='Location 1')


@pytest.fixture
def create_product(create_category, create_location):
    product = Product.objects.create(
        name='Product 1',
        description='Product description',
        price=10.99,
        category=create_category,
        is_available=True
    )
    product.location.set([create_location])
    return product


@pytest.fixture
def product_detail_url(create_product):
    return reverse(
        'catalog:product_detail',
        args=(create_product.id,)
    )
