from django.shortcuts import render
from account.forms import MySignupForm
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# Create your views here.
class UserSignupreq(View):
  template_name = 'signup.html'
  def post(self,request):
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
 



class UserSignupView(TemplateView):
  template_name = 'signup.html'

  def get_context_data(self, **kwargs):
        auth_token = csrf(self.request)
        context = super(UserSignupView, self).get_context_data(**kwargs)
        context['csrf_token'] = auth_token
        return context

class Userconfirm(TemplateView):
    template_name = 'confirm.html'
    


#args.update(csrf(request)),

