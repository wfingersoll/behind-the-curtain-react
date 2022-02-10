from django.shortcuts import render
from django.http import HttpResponse
from .imdb import IMDB
from django.core.exceptions import *
from django.shortcuts import redirect
import collections
import json
from django.http import HttpResponseRedirect
from .wiki import Wiki

class views():

    def index(self, request):
        return render(request, 'myapp/index.html')

    def search(self, request):
        if request.method == 'POST':
            search_title = request.POST.get('textfield', None)
            return redirect('movie/%s' % search_title)
        else:
            return render(request, 'myapp/form.html')

    def titles(self, request):

        return render(request, 'myapp/movie.html')
        
        im = IMDB(search_title)
        movie = im.get_movie_page()
        if(movie == '0'):
            return HttpResponseRedirect('')
        title = im.get_title(movie)
        crew = im.get_crew(movie)
        cast = im.get_cast(movie)
        special_credits = im.get_special_credits(movie)

        context = {'title': title, 'crew': crew, 'cast': cast}

        return render(request, 'myapp/movie.html', context)

    def actor_and_company(self, request, name):

        try:
            wik = Wiki(name)
        except:
            return HttpResponseRedirect('')

        if(wik.name) == 'no results found':
            return HttpResponseRedirect('')

        summary = wik.get_summary()
        agenda = wik.get_agenda()
        views = wik.get_views()
        print(wik.page.url)

        context = {'name': name,
                'summary': summary,
                'agenda': agenda,
                    'views': views,
                }
        return render(request, 'myapp/actor_and_company.html', context)