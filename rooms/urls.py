from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.CreatePhotoView.as_view(), name="add-photos"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.DeletePhotoView.as_view(),
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
