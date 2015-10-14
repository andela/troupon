from django.shortcuts import render
from userprofile.models import UserProfile, STATE_CHOICES
from userprofile.forms import UserProfileForm
from django.core.context_processors import csrf

# Create your views here.
class Userprofileview(TemplateView):
    """class that handles display of the homepage"""

    template_name = "userprofile/profile.html"
    context_var = {
        'show_subscribe': False,
        'show_search': False,
        'states': { 'choices': STATE_CHOICES,  'default': 25 }
    }

    def get(self, request):
        self.context_var.update(csrf(request))
        return render(request, self.template_name, self.context_var)

    def post(self,request):
        
        userprofileform = UserProfileForm(request.POST, instacne=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return HttpresponseRidirect('/') #homepage.
            
