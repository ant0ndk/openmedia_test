from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Page
from .utils import parse_page


class CreatePageView(APIView):
    @swagger_auto_schema(
        operation_description="Создание новой страницы \
            по переданному URL и парсинг заголовков h1, h2, h3 и ссылок",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['url'],
            properties={
                'url': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='URL страницы, \
                                        которую нужно распарсить'),
            }
        ),
        responses={
            200: openapi.Response(
                description="ID созданной страницы",
                examples={
                    'application/json': {
                        'object_id': 1
                    }
                }
            ),
            400: openapi.Response(description="Ошибка валидации URL"),
        }
    )
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        parsed_data = parse_page(url)
        page = Page.objects.create(
            url=url,
            h1_count=parsed_data['h1_count'],
            h2_count=parsed_data['h2_count'],
            h3_count=parsed_data['h3_count'],
            links=parsed_data['links']
        )
        return Response({'object_id': page.id})


@swagger_auto_schema(
    method='get',
    operation_description="Получение информации о странице по её ID",
    responses={
        200: openapi.Response(
            description="Информация о заголовках и ссылках на странице",
            examples={
                'application/json': {
                    'h1': 1,
                    'h2': 2,
                    'h3': 3,
                    'a': ['http://ya.ru/link1', 'http://ya.ru/link2']
                }
            }
        ),
        404: openapi.Response(description="Страница не найдена")
    }
)
@api_view(['GET'])
def get_page(request, object_id):
    try:
        page = Page.objects.get(id=object_id)
    except Page.DoesNotExist:
        return Response({'error': 'Page not found'},
                        status=status.HTTP_404_NOT_FOUND)

    data = {
        'h1': page.h1_count,
        'h2': page.h2_count,
        'h3': page.h3_count,
        'a': page.links
    }
    return Response(data)


@swagger_auto_schema(
    method='get',
    operation_description="Получение списка всех страниц с сортировкой",
    manual_parameters=[
        openapi.Parameter(
            'order', openapi.IN_QUERY,
            description="Сортировка по количеству заголовков h1, h2, h3, \
                либо по времени создания ('created_at'). \
                    Например: order=h1_count или order=-h2_count",
            type=openapi.TYPE_STRING
        ),
    ],
    responses={
        200: openapi.Response(
            description="Список страниц с их заголовками и ссылками",
            examples={
                'application/json': [
                    {
                        'h1': 1,
                        'h2': 2,
                        'h3': 3,
                        'a': ['http://ya.ru/link1', 'http://ya.ru/link2'],
                        'created_at': '2024-10-10T12:00:00Z',
                        'url': 'http://ya.ru'
                    },
                ]
            }
        ),
        400: openapi.Response(description="Некорректный параметр сортировки")
    }
)
@api_view(['GET'])
def list_pages(request):
    order = request.GET.get('order', 'created_at')

    # Определяем допустимые поля для сортировки
    valid_orders = {
        'h1': 'h1_count',
        'h2': 'h2_count',
        'h3': 'h3_count',
        'created_at': 'created_at'
    }

    # Проверяем корректность параметра order
    if order.startswith('-'):
        field = valid_orders.get(order[1:])
        if not field:
            return Response({'error': 'Invalid order parameter'},
                            status=status.HTTP_400_BAD_REQUEST)
        order_by = f'-{field}'
    else:
        field = valid_orders.get(order)
        if not field:
            return Response({'error': 'Invalid order parameter'},
                            status=status.HTTP_400_BAD_REQUEST)
        order_by = field

    # Получаем и сортируем страницы
    pages = Page.objects.all().order_by(order_by)
    result = []

    for page in pages:
        result.append({
            'h1': page.h1_count,
            'h2': page.h2_count,
            'h3': page.h3_count,
            'a': page.links,
            'created_at': page.created_at,
            'url': page.url
        })

    return Response(result)
