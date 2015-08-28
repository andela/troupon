from django.shortcuts import render


# Create your views here.
def landing(request):
    return render(request, 'base.html', {'show_subscribe': True})
