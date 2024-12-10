import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse
from PIL import Image
import pytest

from .constants import (
    CATEGORY_NAME,
    CATEGORY_SLUG,
    EMAIL_AUTHOR,
    FIRST_NAME,
    LAST_NAME,
    LOCATION_NAME,
    QUALITY_STARS,
    REVIEW_CONTENT,
    TASTE_STARS,
    TITLE_REVIEW,
    USERNAME,
)
from catalog.models import Category, Location, Product, Review


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
        name=CATEGORY_NAME, slug=CATEGORY_SLUG
    )


@pytest.fixture
def category_product_list_url(create_category):
    return reverse(
        'catalog:category_product_list',
        args=(create_category.slug,)
    )


@pytest.fixture
def create_location():
    return Location.objects.create(name=LOCATION_NAME)


# Delete images created
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


@pytest.fixture
def product_review_url(create_product):
    return reverse(
        'catalog:review_form',
        args=(create_product.id,)
    )


@pytest.fixture
def create_review(create_product, author, create_location):
    review = Review.objects.create(
        title=TITLE_REVIEW,
        review=REVIEW_CONTENT,
        taste_stars=TASTE_STARS,
        quality_stars=QUALITY_STARS,
        product=create_product,
        user=author,
        location=create_location
    )
    return review


@pytest.fixture
def product_update_review_url(create_review):
    return reverse(
        'catalog:review_update',
        args=(create_review.product.id, create_review.id)
    )


@pytest.fixture
def product_delete_review_url(create_review):
    return reverse(
        'catalog:review_delete',
        args=(create_review.product.id, create_review.id)
    )


@pytest.fixture
def profile_url(author):
    return reverse(
        'users:profile',
        args=(author.username,)
    )


@pytest.fixture
def profile_update_url(author):
    return reverse(
        'users:profile_update',
        args=(author.username,)
    )


@pytest.fixture
def profile_create_address_url():
    return reverse(
        'users:address_create'
    )

# create address user fixture
# create profile_update_direction_fixture
# create profile_delete_direction_fixture
