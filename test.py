import payplug
from pprint import pprint
import datetime

payplug.set_secret_key('sk_test_61b66879f4bdc6795e3d7dc37c7a6343')

# Retrieve payment
# payment = payplug.Payment.retrieve('pay_Xjp6SVPI2YwgCGck5U5bL')

# Create payment
# payment_data = {
#     'amount': 3300,
#     'currency': 'EUR',
#     'customer': {
#         'email': 'john.watson@example.net',
#         'first_name': 'John',
#         'last_name': 'Watson'
#     },
#     'hosted_payment': {
#         'return_url': 'http://google.fr',
#         'cancel_url': 'http://google.fr',
#     },
#     'notification_url': 'http://google.fr',
#     'metadata': {
#         'customer_id': '58790'
#     },
#     'force_3ds': True
# }
# payment = payplug.Payment.create(**payment_data)

# List payments
# payments = payplug.Payment.list(per_page=2)
# for payment in payments:
#     pprint(payment)

# API DOC TESTS

########################
# per_page = 1
# page = 1
# payments = payplug.Payment.list()
# pprint(payments.data)
# for payment in payments:
#     pprint(payment)
#########################

########################
# request_body = b'{"id": "pay_3LXfORVnmEudP0kfTXhO6z", "object": "payment"}'  # This line may depend on your framework.
# # request_body = '{"id": "pay_3LXfORVnmEudP0kfTXhO6z", "object": "payment"}'  # This line may depend on your framework.
# try:
#     resource = payplug.notifications.treat(request_body)
# except payplug.exceptions.PayplugError:
#     # Handle errors
#     print('error')
# else:
#     if resource.object == 'payment' and resource.is_paid:
#         # Process the paid payment
#         pprint(resource)
#     elif resource.object == 'refund':
#         # Process the refund
#         pprint(resource)
#########################

#########################
# payment = next(payplug.Payment.list())
# # Get an attribute of the payment object:
# print(str(payment.amount))  # Print the payment amount
# print(str(payment.id))  # Print the payment id
# # Print the payment creation time in an human readable way
# print(datetime.datetime.fromtimestamp(payment.created_at).strftime('%d/%m/%Y %H:%M:%S'))
#
# # Chain relations between objects:
# print(payment.hosted_payment.payment_url)  # Print the payment URL
# print(payment.customer.email)  # Print the customer email
#
# # Retrieve metadata
# print(payment.metadata['customer_id'])
#########################

##############################
# payment_data = {
#     'amount': 3300,
#     'currency': 'EUR',
#     'customer': {
#         'email': 'john.watson@example.net',
#         'first_name': 'John',
#         'last_name': 'Watson',
#     },
#     'hosted_payment': {
#         'return_url': 'https://www.example.net/success?id=42710',
#         'cancel_url': 'https://www.example.net/cancel?id=42710',
#     },
#     'notification_url': 'https://www.example.net/notifications.php?id=42710',
#     'metadata': {
#         'customer_id': 42710,
#     },
# }
# payment = payplug.Payment.create(**payment_data)
##############################

#######################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
# pprint(payment)
#######################################

#######################################
# payments = payplug.Payment.list()
# payment = next(payments)
# pprint(payment)
#######################################

######################################

######################################
# payment = payplug.Payment.retrieve('pay_3LXfORVnmEudP0kfTXhO6z')
# pprint(payment.list_refunds().data[0].id)
###############################

########################################
# refund = payplug.Refund.retrieve('pay_3LXfORVnmEudP0kfTXhO6z', 're_3nJ98Ct8KuI9CBkbbwMHK2')
# # Print the amount of the refund
# print(str(refund.amount))
# # Print the refund creation time in an human readable way
# print(datetime.datetime.fromtimestamp(refund.created_at).strftime('%d/%m/%Y %H:%M:%S'))
########################################

#######################################
# payment_id = 'pay_Xjp6SVPI2YwgCGck5U5bL'
# refund_data = {
#     'amount': 358,
#     'metadata': {
#         'customer_id': 42710,
#         'reason': 'The delivery was delayed',
#     },
# }
# refund = payplug.Refund.create(payment_id, **refund_data)
#######################################

########################################
# payment = payplug.Payment.retrieve('pay_Xjp6SVPI2YwgCGck5U5bL')
# refund_data = {'amount': 100}
# refund = payment.refund(**refund_data)
########################################

########################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
# refund = payment.refund()
########################################


########################################
# # Retrieve a refund object from its id and its payment id
# payment_id = 'pay_hzZkH5SfA2ZTufdnpUOOz'
# refund_id = 're_4BjxCYTOjxRlL6i11YhSah'
# pprint(payplug.Refund.retrieve(payment_id, refund_id))
########################################

#########################################
# payment_id = 'pay_hzZkH5SfA2ZTufdnpUOOz'
# refunds = payplug.Refund.list(payment_id)
# refund = refunds.data[0]
# pprint(refund)
########################################

#########################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
# refunds = payment.list_refunds()
# refund = refunds.data[0]
# pprint(refund)
########################################

#########################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
# refunds = payment.list_refunds()
# for refund in refunds:
#     print(str(refund.id))
########################################

#########################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
# refunds = payment.list_refunds()
# for refund in refunds:
#     print(str(refund.id))
########################################

########################################
# payment_data = {
#     'amount': 1500,
#     'currency': 'EUR',
#     'customer': {
#         'email': 'jean.bouon@example.net',
#         'first_name': 'Jean',
#         'last_name': 'Bouon',
#     },
#     'hosted_payment': {
#         'return_url': 'http://example.net/success?id=MSSD004567FR',
#         'cancel_url': 'http://example.net/cancel?id=MSSD004567FR',
#     },
#     'notification_url': 'http://example.net/notifications?id=MSSD004567FR',
#     'metadata': {
#         'customer_id': 'MSSD004567FR',
#         'product_id': 'ts_green_004',
#     },
# }
# payment = payplug.Payment.create(**payment_data)
# payment_url = payment.hosted_payment.payment_url
# pprint(payment_url)
########################################

########################################
# payment = payplug.Payment.retrieve('pay_hzZkH5SfA2ZTufdnpUOOz')
#
# # Display informations about the payment:
# print('Amount: ' + str(payment.amount / 100.) + ' €')
# print('Payment Id: ' + str(payment.id))
# print('Is paid: ' + str(payment.is_paid))
#
# creation_date = datetime.datetime.fromtimestamp(payment.created_at)
# creation_date_str = creation_date.strftime('%d/%m/%Y %H:%M:%S')
# print('Creation date: ' + creation_date_str)
# paid_at = datetime.datetime.fromtimestamp(payment.hosted_payment.paid_at)
# paid_at_str = paid_at.strftime('%d/%m/%Y %H:%M:%S')
# print('Paid at: ' + paid_at_str)
#
# print('First name: ' + payment.customer.first_name)
# print('Last Name: ' + payment.customer.last_name)
# print('E-mail: ' + payment.customer.email)
#
# print('Customer Id: ' + str(payment.metadata['customer_id']))
########################################

###########################################
payments = payplug.Payment.list()

for payment in payments:
    print('Amount: ' + str(payment.amount / 100.) + ' €')
    print('Payment Id: ' + str(payment.id))
    print('Is paid: ' + str(payment.is_paid))

    creation_date = datetime.datetime.fromtimestamp(payment.created_at)
    creation_date_str = creation_date.strftime('%d/%m/%Y %H:%M:%S')
    print('Creation date: ' + creation_date_str)
    paid_at = payment.hosted_payment.paid_at
    if paid_at:
        paid_at = datetime.datetime.fromtimestamp(paid_at)
        paid_at_str = paid_at.strftime('%d/%m/%Y %H:%M:%S')
        print('Paid at: ' + paid_at_str)

    print('First name: ' + payment.customer.first_name)
    print('Last Name: ' + payment.customer.last_name)
    print('E-mail: ' + payment.customer.email)
##########################################
