from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('members/<str:id>', views.members, name="members"),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('logout/', views.logout, name='logout'),
    path('addMember/', views.addMember, name='addMember'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)