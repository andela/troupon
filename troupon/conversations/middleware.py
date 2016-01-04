from conversations.models import Message


class UnreadMessageCount(object):
    """Update response context data with the count of unread messages
    """
    def process_template_response(self, request, response):
        context_data = {
            'unread_mesg_count': Message.unread_count(request)
        }
        response.context_data.update(context_data)
        return response
