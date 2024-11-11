# blog_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_commentario/<int:post_id>/', views.add_comentario, name='add_commentario'),
    path('editar_comentario/<int:post_id>/<int:comment_id>/', views.editar_comentario, name='editar_comentario'),
    path('deletar_comentario/<int:post_id>/<int:comment_id>/', views.deletar_comentario, name='deletar_comentario'),
]
