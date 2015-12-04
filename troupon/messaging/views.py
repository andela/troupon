from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages as alert
from django.template.defaultfilters import slugify
from django.template.response import TemplateResponse
from .models import Message


class DispatchView(View):
    """Delivers message to recipients"""

    def post(self, request, action, *args, **kwargs):
        """dispatch message"""
        recipient_username = request.POST.get('recipient') or 'admin'
        recipient = User.objects.get(username=recipient_username)
        message = None
        if action == 'new':
            payload = {
                'subject': request.POST.get('subject'),
                'sender': User.objects.get(username=request.user.username),
                'body': request.POST.get('body'),
                'recipient': recipient,
            }  # create new message payload
            message = Message(**payload)
            message.sent_at = timezone.now()
            message.save()
        if action == 'reply':
            parent_msg_id = request.POST.get('parent_msg')
            message = Message.objects.get(id=parent_msg_id)
            message.replied_at = timezone.now()
            message.save()  # update replied at

            payload = {
                'sender': User.objects.get(username=request.user.username),
                'parent_msg': message,
                'body': request.POST.get('body'),
                'recipient': recipient,
            }  # create reply payload
            reply = Message(**payload)
            reply.sent_at = timezone.now()
            reply.save()

            alert.add_message(
                request, alert.SUCCESS, 'Message sent successfully.')

        return redirect(
            reverse(
                'read_message',
                kwargs={
                 'id': message.id,
                 'slug': slugify(message.subject)
                }
            )
        )


class ReadView(View):

    def get(self, request):
        user_id = request.user.id
        messages = Message.objects.extra(
            where=['recipient_id={} OR sender_id={}'.format(user_id, user_id)]
        ).filter(parent_msg=None).order_by('-sent_at')
        context_data = {'messages': messages}
        if request.user.is_superuser:
            context_data['users'] = User.objects.exclude(is_superuser=True)
        return TemplateResponse(request, 'messaging/index.html', context_data)


class ReadFromUserView(View):

    def get(self, request, sender):
        """Retrievers mail from a specific user
        """
        recipient = User.objects.get(username=request.user.username)
        sender = User.objects.get(username=sender)
        messages = Message.objects.filter(recipient=recipient, sender=sender)
        context_data = {'messages': messages}
        return TemplateResponse(request, 'messaging/index.html', context_data)


class ReadDetailView(View):

    def get(self, request, id, slug):
        mesg = Message.objects.get(id=id)
        mesg.read_at = timezone.now()
        mesg.save()

        other_messages = Message.objects.filter(
                parent_msg=mesg.id).order_by('-sent_at')

        other_messages.update(read_at=mesg.read_at)

        context_data = {
            'mesg': mesg,
            'other_messages': other_messages
        }
        return TemplateResponse(request, 'messaging/detail.html', context_data)
