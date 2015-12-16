from conversations.models import Message


class UnreadMessageCount(object):
    """Update response context data with the count of unread messages
    """
    def process_template_response(self, request, response):
        context_data = {
            'unread_mesg_count': Message.objects.filter(
                recipient=request.user.id).filter(read_at=None).count()
        }
        response.context_data.update(context_data)
        return response
