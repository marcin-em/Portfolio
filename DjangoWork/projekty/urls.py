from django.urls import path

from .views import (
    project_list_view,
    project_create_view,
    project_detail_view,
    project_update_view,
    project_delete_view,
)

urlpatterns = [
    path('projects/', project_list_view),
    path('project/new/', project_create_view),
    path('project/<int:project_id>/', project_detail_view),
    path('project/<int:project_id>/edit/', project_update_view),
    path('project/delete/<int:project_id>/', project_delete_view)
]
