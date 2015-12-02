from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from .models import Message
from datetime import datetime


class PostManDispatchView(View):
    """Delivers message to recipients"""

    def post(self, request, action, *args, **kwargs):
        """dispatch message"""
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)
        if action == 'new':
            payload = {
                'subject': request.POST.get('subject'),
                'sender': User.objects.get(username=request.user.username),
                'body': request.POST.get('body'),
                'recipient': recipient,
            }  # create new message payload
            message = Message(**payload)
            message.sent_at = datetime.now()
            message.save()
        if action == 'reply':
            parent_msg_id = request.POST.get('parent_msg')
            parent_msg = Message.objects.get(id=parent_msg_id)
            parent_msg.replied_at = datetime.now()
            parent_msg.save()
            payload = {
                'sender': User.objects.get(username=request.user.username),
                'parent_msg': parent_msg,
                'body': request.POST.get('body'),
                'recipient': recipient,
            }  # create reply payload
            message = Message(**payload)
            message.save()

        return redirect(reverse('read_message'))


class PostManReadView(View):

    def get(self, request):
        recipient = User.objects.get(username=request.user.username)
        messages = Message.objects.filter(recipient=recipient).order_by('-sent_at')
        context_data = {'messages': messages}
        return render(request, 'messaging/index.html', context_data)


class PostManReadFromUserView(View):

    def get(self, request, sender):
        """Retrievers mail from a specific user
        """
        recipient = User.objects.get(username=request.user.username)
        sender = User.objects.get(username=sender)
        messages = Message.objects.filter(recipient=recipient, sender=sender)
        context_data = {'messages': messages}
        return render(request, 'messaging/index.html', context_data)
