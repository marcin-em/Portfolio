from django.urls import path

from .views import (
    client_list_view,
    client_create_view,
    client_detail_view,
    client_update_view,
    client_delete_view
)

urlpatterns = [
    path('clients/', client_list_view),
    path('client/new/', client_create_view),
    path('client/<int:client_id>/', client_detail_view),
    path('client/<int:client_id>/edit/', client_update_view),
    path('client/delete/<int:client_id>/', client_delete_view),
]
