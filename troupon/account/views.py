from django.shortcuts import render
from account.forms import MySignupForm
from django.views.generic.base import TemplateView
from django.core.context_processors import csrf

# Create your views here.
def UserSignupreq(request):
    if request.method == 'POST':
        MySignupForm.username = MySignupForm(request.POST.get('username',''))
        MySignupForm.email = MySignupForm(request.POST.get('email',''))
        MySignupForm.first_name = MySignupForm(request.POST.get('first_name',''))
        MySignupForm.last_name = MySignupForm(request.POST.get('last_name',''))
        MySignupForm.password = MySignupForm(request.POST.get('password',''))
        MySignupForm.confirm_password = MySignupForm(request.POST.get('confirm_password',''))
        if MySignupForm.is_valid():
            MySignupForm.save()
            return HttpResponseRedirect('/auth/confirm/')

    else:
      return HttpResponseRedirect('/auth/signup/')



class UserSignup(TemplateView):
  template_name = signup.html

  def get_context_data(self, **kwargs):
        context = super(UserSignup, self).get_context_data()
        return context




