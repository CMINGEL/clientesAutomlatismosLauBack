from django.urls import path
from . import views 
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

#Subir documentos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ejecutivos/', views.ejecutivos.as_view(), name='ejecutivos'),
    path('ejecutivos/<str:pk>/', views.ejecutivos.as_view(), name='ejecutivosDelete'),
    path('clientes/', views.clientes.as_view(), name='clientes'),
    path('clientes/<str:pk>/', views.clientes.as_view(), name='clientesBorrar'),
    path('registrar/', views.Register.as_view(), name='registrar' ),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('servicios/', views.Servicios.as_view(), name='ServiciosView'),
    path('servicios/<int:pk>/', views.Servicios.as_view()),

    path('subirarchivos/', views.simple_upload.as_view(), name='subirArchivos'),
    path('subirarchivos/<int:pk>/', views.simple_upload.as_view(), name='verArchivos'),

    path('registros/', views.descargaxls, name='registros'),
    path('ejecutivosT/', views.ejecutivosT.as_view(), name='ejecutivos'),
]

#Subir documentos
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)