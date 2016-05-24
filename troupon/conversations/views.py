from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import View
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib import messages as alert
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from conversations.models import Message, MESG_CHOICES


class ComposeMessageView(View):
    """Composes messages sent to a recipient"""
    def get(self, request):
        """Show compose view"""
        context_data = {}
        if request.user.is_superuser:
            # grant admin access to list of all registered users
            #  in the response context
            context_data.update({
                'users': User.objects.exclude(is_superuser=True)
            })
        else:
            context_data.update({
                'users': User.objects.filter(is_superuser=True)
            })
        context_data.update({
            'breadcrumbs': [
                {'name': 'Merchant', 'url': reverse('account')},
                {'name': 'Messages', 'url': reverse('messages')},
                {'name': 'Compose', 'url': reverse('compose_message')},
            ],
            'message_choices': MESG_CHOICES,
        })
        return TemplateResponse(
            request, 'conversations/compose.html', context_data
        )


class MessagesView(View):
    """Views messages for a sender"""
    def get(self, request):
        """Read thread topics"""
        u_id = request.user.id
        mesgs = Message.objects.filter(
            Q(recipient=u_id) | Q(sender=u_id)
        ).exclude(~Q(parent_msg=None)).order_by('-sent_at')
        context_data = {
            'breadcrumbs': [
                {'name': 'Merchant', 'url': reverse('account')},
                {'name': 'Messages', 'url': reverse('messages')},
            ],
            'mesgs': mesgs,
        }
        return TemplateResponse(
            request, 'conversations/index.html', context_data
        )

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
                'message', kwargs={'m_id': mesg.id}
            )
        )


class MessageView(View):
    """View messages in a thread """
    def get(self, request, m_id):
        """Read messages in a conversation"""
        time_now = timezone.now()
        mesg = Message.objects.filter(Q(id=m_id) | Q(parent_msg=m_id))
        latest_mesg = mesg.latest('sent_at')
        other_messages = mesg.exclude(id=latest_mesg.id)
        is_recipient = latest_mesg.recipient == request.user
        # is_recipient = mesg.recipient == request.user

        if is_recipient:  # value comparison
            latest_mesg.read_at = time_now
            latest_mesg.save()
        # get messages in thread
        if other_messages:
            other_messages = other_messages.order_by('-sent_at')
            # update last read time for messages in thread
            other_messages.update(read_at=time_now)
        mesg = other_messages.first()
        context_data = {
            'mesg': latest_mesg,
            'other_messages': other_messages,
            'breadcrumbs': [
                {'name': 'Merchant', 'url': reverse('account')},
                {'name': 'Messages', 'url': reverse('messages')},
                {'name': latest_mesg.subject or latest_mesg
                    .parent_msg.subject},
            ]
        }
        return TemplateResponse(
            request, 'conversations/detail.html', context_data
        )

    def post(self, request, m_id):
        """Dispatch a reply to a conversation"""
        recipient_username = request.POST.get('recipient') or 'admin'
        recipient = User.objects.get(username=recipient_username)
        parent_msg_id = request.POST.get('parent_msg')

        message = Message.objects.get(id=int(parent_msg_id))
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
                'message', kwargs={'m_id': message.id}
            )
        )
