import datetime

from django.shortcuts import render

# Create your views here.
def index(request):
    context ={
        'nav': 'index',
        'midday': datetime.time(12),
        'evening': datetime.time(18)
    }
    return render(request, 'main/index.html', context)

def about(request):
    return render(request, 'main/about.html', {'nav': 'about'})
