from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .models import Author, Tag, Quote


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'quotes/password_reset.html'
    email_template_name = 'quotes/password_reset_email.html'
    html_email_template_name = 'quotes/password_reset_email.html'
    success_url = reverse_lazy('quotes:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'quotes/password_reset_subject.txt'


def main(request, page=1):
	quotes = Quote.objects.all()
	per_page = 10
	paginator = Paginator(list(quotes), per_page)
	quotes_on_page = paginator.page(page)
	return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


def author_detail(request, author_fullname):
    author = get_object_or_404(Author, fullname=author_fullname)
    return render(request, 'quotes/author_detail.html', context={'author': author})


def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    return render(request, 'quotes/tag_detail.html', context={'tag': tag})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('quotes:root')
    return render(request, 'quotes/registration.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quotes:root')
    return render(request, 'quotes/login.html')


def user_logout(request):
    logout(request)
    return redirect('quotes:root')


def add_author(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        born_date = request.POST.get('born_date')
        born_location = request.POST.get('born_location')
        description = request.POST.get('description')
        
        Author.objects.create(fullname=fullname, born_date=born_date, born_location=born_location, description=description)
        
        return redirect('quotes:root')
    
    return render(request, 'quotes/add_author.html')


def add_quote(request):
    if request.method == 'POST':
        quote_text = request.POST.get('quote')
        author_id = request.POST.get('author')
        tag_names = request.POST.getlist('tags')
        
        author = Author.objects.get(pk=author_id)
        quote = Quote.objects.create(quote=quote_text, author=author)
        
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)
        
        return redirect('quotes:root')
        
    authors = Author.objects.all()
    tags = Tag.objects.all()
    return render(request, 'quotes/add_quote.html', {'authors': authors, 'tags': tags})
