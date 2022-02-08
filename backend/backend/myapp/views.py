from django.shortcuts import render
from django.http import HttpResponse
from .imdb import IMDB
from django.core.exceptions import *
from django.shortcuts import redirect
import collections
import json
from django.http import HttpResponseRedirect
from .wiki import Wiki

def index(request):
    return render(request, 'myapp/index.html')

def search(request):
    if request.method == 'POST':
        search_title = request.POST.get('textfield', None)
        return redirect('movie/%s' % search_title)
    else:
        return render(request, 'form.html')

def movie(request, search_title):

    im = IMDB(search_title)
    movie = im.get_movie_page()
    if(movie == '0'):
        return HttpResponseRedirect('/playground/index')
    title = im.get_title(movie)
    crew = im.get_crew(movie)
    cast = im.get_cast(movie)
    special_credits = im.get_special_credits(movie)

    context = {'title': title, 'crew': crew, 'cast': cast}

    return render(request, 'movie.html', context)

def actor_and_company(request, name):

    try:
        wik = Wiki(name)
    except:
        return HttpResponseRedirect('/playground/index')

    if(wik.name) == 'no results found':
        return HttpResponseRedirect('/playground/index')

    summary = wik.get_summary()
    agenda = wik.get_agenda()
    views = wik.get_views()
    print(wik.page.url)

    context = {'name': name,
               'summary': summary,
               'agenda': agenda,
                'views': views,
               }
    return render(request, 'actor_and_company.html', context)