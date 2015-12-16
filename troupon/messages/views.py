from django.http import Http404
from django.utils import timezone
from messages.models import Message
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages as alert
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse


class MessagesView(View):

    def get(self, request):
        """Read thread topics"""
        user_id = request.user.id
        mesgs = Message.objects.extra(
            where=['recipient_id={} OR sender_id={}'.format(user_id, user_id)]
        ).filter(parent_msg=None).order_by('-sent_at')
        context_data = {'messages': mesgs}
        if request.user.is_superuser:
            # grant admin access to list of all registered users
            #  in the response context
            context_data['users'] = User.objects.exclude(is_superuser=True)
        return TemplateResponse(request, 'messaging/index.html', context_data)

    def post(self, request, *args, **kwargs):
        """Dispatch message to start a new conversation"""
        recipient_username = request.POST.get('recipient') or 'admin'
        recipient = User.objects.get(username=recipient_username)
        payload = {
            'subject': request.POST.get('subject'),
            'sender': User.objects.get(username=request.user.username),
            'body': request.POST.get('body'),
            'recipient': recipient,
        }  # create new message payload

        mesg = Message(**payload)
        mesg.sent_at = timezone.now()
        mesg.save()

        alert.add_message(
            request, alert.SUCCESS, 'New conversation started with {}.'
            .format(recipient.username)
        )

        return redirect(
            reverse(
                'message', kwargs={'id': mesg.id}
            )
        )


class MessageView(View):

    def get(self, request, id):
        """Read messages in a conversation"""
        mesg = Message.objects.get(id=id)

        if mesg.parent_msg:
            raise Http404("Oops! You shouldn't mess around with URLs")
        mesg.read_at = timezone.now()  # update last read time
        mesg.save()

        # get messages in thread
        other_messages = Message.objects\
            .filter(parent_msg=mesg.id).order_by('-sent_at')

        # update last read time for messages in thread
        other_messages.update(read_at=mesg.read_at)

        context_data = {
            'mesg': mesg,
            'other_messages': other_messages
        }
        return TemplateResponse(request, 'messages/detail.html', context_data)

    def post(self, request, m_id):
        """Dispatch a reply to a conversation"""
        recipient_username = request.POST.get('recipient') or 'admin'
        recipient = User.objects.get(username=recipient_username)
        parent_msg_id = request.POST.get('parent_msg')
        message = Message.objects.get(id=parent_msg_id)
        message.replied_at = timezone.now()
        message.save()  # update replied at
        parent_msg_id = Message.objects.get(id=m_id)

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
            request, alert.SUCCESS, 'Message sent successfully.'
        )

        return redirect(
            reverse(
                'message', kwargs={'id': message.id}
            )
        )
