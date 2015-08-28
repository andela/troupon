from django.shortcuts import render,render_to_response


# Create your views here.
def landing(request):
    return render(request, 'base.html', {'show_subscribe': True})


def signup(request):
    return render_to_response('signin_register.html')
