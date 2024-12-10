from http import HTTPStatus
from django.urls import reverse

import pytest
from pytest_lazyfixture import lazy_fixture


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        lazy_fixture('index_url'),
        lazy_fixture('about_us_url'),
        lazy_fixture('category_url'),
        lazy_fixture('category_product_list_url'),
        lazy_fixture('product_detail_url'),
    )
)
def test_get_routes_availability_for_anonymous_user(client, name):
    response = client.get(name)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, expected_redirect',
    (
        (
            lazy_fixture('product_review_url'),
            reverse('login')+'?next='+reverse('catalog:review_form', args=(1,))
        ),
        (
            lazy_fixture('product_update_review_url'),
            reverse('catalog:product_detail', args=(1,))
        ),
        (
            lazy_fixture('product_delete_review_url'),
            reverse('catalog:product_detail', args=(1,))
        ),
        (
            lazy_fixture('profile_url'),
            reverse('pages:index')
        ),
        (
            lazy_fixture('profile_update_url'),
            reverse('pages:index')
        ),
        (
            lazy_fixture('profile_create_address_url'),
            reverse('login')+'?next='+reverse('users:address_create')
        ),
    )
)
def test_redirects_for_anonymous_user(client, name, expected_redirect):
    response = client.get(name)
    assert response.status_code == HTTPStatus.FOUND
    assert response['Location'] == expected_redirect


# tests for review edit delete by another author


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    (
        lazy_fixture('index_url'),
        lazy_fixture('about_us_url'),
        lazy_fixture('category_url'),
        lazy_fixture('category_product_list_url'),
        lazy_fixture('product_detail_url'),
        lazy_fixture('product_review_url'),
        lazy_fixture('product_update_review_url'),
        lazy_fixture('product_delete_review_url'),
        lazy_fixture('profile_url'),
        lazy_fixture('profile_update_url'),
        lazy_fixture('profile_create_address_url'),
    )
)
def test_get_routes_availability_for_auth_user(author_client, name):
    response = author_client.get(name)
    assert response.status_code == HTTPStatus.OK
