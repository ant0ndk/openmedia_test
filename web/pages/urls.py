from django.urls import path
from .views import CreatePageView, get_page, list_pages

urlpatterns = [
    path('page/create', CreatePageView.as_view(), name='create_page'),
    path('page/<int:object_id>', get_page, name='get_page'),
    path('page/list', list_pages, name='list_pages'),
]
