# blog_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json

def index(request):
    smartphone = {
        "name": "Samsung Galaxy S23 Ultra",
        "data": {
            "year": 2023,
            "price": 1199.99,
            "CPU_model": "Snapdragon 8 Gen 2",  
            "Storage": "512 GB",
            "img": "https://www.lavanguardia.com/andro4all/hero/2023/04/galaxy-s23-vs-galaxy-s23-ultra-portada.jpg?width=1200&aspect_ratio=16:9",
            "comments": [
                {"author": "Ana Souza", "comment": "Excelente câmera e desempenho!"},
                {"author": "Pedro Lima", "comment": "A bateria dura o dia todo!"}
            ]
        }
    }

    smartwatch = {
        "name": "Apple Watch Series 9",
        "data": {
            "year": 2023,
            "price": 399.99,
            "CPU_model": "Apple S9 Chip",  
            "Battery_life": "18 hours", 
            "img": "https://www.apple.com/newsroom/images/2023/09/apple-introduces-the-advanced-new-apple-watch-series-9/article/Apple-Watch-S9-display-2000-nits-230912_big.jpg.large.jpg",
            "comments": [
                {"author": "João Oliveira", "comment": "Ótimo para monitoramento de saúde."},
                {"author": "Marina Silva", "comment": "Compatível com muitos apps!"}
            ]
        }
    }

    response1 = requests.post("https://api.restful-api.dev/objects", json=smartphone)
    response2 = requests.post("https://api.restful-api.dev/objects", json=smartwatch)

    posts = [response1.json(), response2.json()]
    
    return render(request, "blog.html", {"posts": posts})

#funções em teste

def add_comentario(request, post_id):
    
    if request.method == 'POST':
        new_comment = {
            "author": request.POST.get("author"),
            "comment": request.POST.get("comment")
        }
        
        # Procurar o post pelo ID e adicionar o comentário
        post = next((post for post in posts if post["id"] == post_id), None)
        if post:
            post["data"]["comments"].append(new_comment)
        return redirect('index')
    
    return render(request, 'add_comentario.html', {'post_id': post_id})

def editar_comentario(request, post_id, comment_id):
    
    post = next((post for post in posts if post["id"] == post_id), None)
    if not post:
        return JsonResponse({"error": "Post not found"}, status=404)

    comment = post["data"]["comments"][comment_id] if comment_id < len(post["data"]["comments"]) else None
    if not comment:
        return JsonResponse({"error": "Comment not found"}, status=404)

    if request.method == 'POST':
        comment["author"] = request.POST.get("author", comment["author"])
        comment["comment"] = request.POST.get("comment", comment["comment"])
        return redirect('index')
    
    return render(request, 'editar_comentario.html', {'post_id': post_id, 'comment_id': comment_id})

def deletar_comentario(request, post_id, comment_id):
    post = next((post for post in posts if post["id"] == post_id), None)
    if not post:
        return JsonResponse({"error": "Post not found"}, status=404)

    if 0 <= comment_id < len(post["data"]["comments"]):
        del post["data"]["comments"][comment_id]
    return redirect('index')


