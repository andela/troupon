from django.views.generic.base import TemplateView

# Create your views here.

class ForgotPasswordView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hi, This is just a placeholder for forgot_password.html')