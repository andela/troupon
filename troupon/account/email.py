# import requests

# def send_email(sender, reciepient, subject, text=None, html=None):
#     app = current_app._get_current_object()
#     response = requests.post(
#         "https://api.mailgun.net/v3/mailgun.mcbella.com.ng/messages", 
#         auth=("api", "key-e75e2753c478e22772ab5d30dc4171c4"), 
#         data={
#             "from": sender,
#             "to": reciepient,
#             "subject": subject,
#             "text": text,
#             "html": html
#         }
#     )
#     # response.raise_for_status()
#     return response
