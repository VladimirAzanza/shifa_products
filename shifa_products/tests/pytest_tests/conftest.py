import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
from PIL import Image
import pytest

from .constants import EMAIL_AUTHOR, FIRST_NAME, LAST_NAME, USERNAME
from catalog.models import Category, Location, Product


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        email=EMAIL_AUTHOR,
        username=USERNAME,
        first_name=FIRST_NAME,
        last_name=LAST_NAME
    )


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


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
def create_image():
    image = Image.new('RGB', (100, 100), color='red')
    image_file = io.BytesIO()
    image.save(image_file, format='JPEG')
    image_file.seek(0)
    image_name = 'pytest_image.jpg'
    return SimpleUploadedFile(
        image_name, image_file.read(), content_type='image/jpeg'
    )


@pytest.fixture
def create_product(create_category, create_location, create_image):
    product = Product.objects.create(
        name='Product 1',
        description='Product description',
        image=create_image,
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
