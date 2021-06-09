# from django.conf import settings
# from django.core.mail import send_mail
from django.shortcuts import render
from .models import Recipe, Tag
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 2)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


# send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER,
#           ['vadim624790@mail.ru'])
