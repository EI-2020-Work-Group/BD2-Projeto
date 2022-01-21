from django.urls import path
from projeto import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('post/create', views.post_create, name='post_create'),
    path('groups', views.groups, name='groups'),
    path('group/<int:id>', views.group, name='group'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)