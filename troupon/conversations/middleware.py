from conversations.models import Message
from django.http import HttpResponse


class UnreadMessageCount(object):
    """Update response context data with the count of unread messages
    """
    def process_template_response(self, request, response):
        if request.path.startswith('/api/'):
            context_data = {
                'unread_mesg_count': 0
            }
            response.context_data = context_data
            return response
        else:
            context_data = {
                'unread_mesg_count': Message.unread_count(request)
            }
            response.context_data.update(context_data)
            return response
