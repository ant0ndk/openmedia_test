from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Page


class PageAPITests(APITestCase):
    def setUp(self):
        # Настройка тестов, если необходимо
        self.create_url = reverse('create_page')
        self.get_url = lambda object_id: reverse('get_page', args=[object_id])
        self.list_url = reverse('list_pages')

    def test_create_page_success(self):
        """Тест на успешное создание страницы."""
        response = self.client.post(self.create_url, {'url': 'http://ya.ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_id', response.data)

        # Проверяем, что страница была создана
        self.assertTrue(Page.objects.filter(
            id=response.data['object_id']).exists())

    def test_create_page_invalid_url(self):
        """Тест на создание страницы с недопустимым URL."""
        response = self.client.post(self.create_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'URL is required')

    def test_get_page_success(self):
        """Тест на успешное получение информации о странице по ID."""
        response = self.client.post(self.create_url, {'url': 'http://ya.ru'})
        object_id = response.data['object_id']

        response = self.client.get(self.get_url(object_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('h1', response.data)

    def test_get_page_not_found(self):
        """Тест на получение страницы с несуществующим ID."""
        response = self.client.get(self.get_url(9999))  # Несуществующий ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Page not found')

    def test_list_pages_success(self):
        """Тест на успешное получение списка страниц."""
        self.client.post(self.create_url, {'url': 'http://ya.ru'})
        self.client.post(self.create_url, {'url': 'http://google.com'})

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_list_pages_order(self):
        """Тест на получение списка страниц с сортировкой по h1."""
        self.client.post(self.create_url, {'url': 'http://ya.ru'})
        self.client.post(self.create_url, {'url': 'http://google.com'})

        response = self.client.get(self.list_url, {'order': 'h1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Здесь можно добавить дополнительные проверки по сортировке,
        # если известно, сколько h1 на каждой странице

    def test_list_pages_invalid_order(self):
        """
        Тест на получение списка страниц
        с некорректным параметром сортировки.
        """
        response = self.client.get(self.list_url, {'order': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid order parameter')
