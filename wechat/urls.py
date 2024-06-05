from django.urls import path
from . import views


urlpatterns = [
    path('' , views.index , name='index'),
    path("<str:room_name>/", views.room, name="room"),
    path("new_room" , views.create_room , name='create_room')

]