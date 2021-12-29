# -*- coding: utf-8 -*-
from payplug.resources import InstallmentPlan, Payment
from payplug.test import TestBase


class TestInstallmentPlansResource(TestBase):
    def test_initializer_installment_plans(self):

        null = None
        true = True
        false = False

        installment_plan_attributes = {
            "id": "inst_1FTGSRWYHla7eDkfTo2Usd",
            "object": "installment_plan",
            "is_live": true,
            "is_active": true,
            "currency": "EUR",
            "created_at": 1548326773,
            "is_fully_paid": false,
            "billing": {
                "title": "mr",
                "first_name": "John",
                "last_name": "Watson",
                "email": "john.watson@example.net",
                "mobile_phone_number": null,
                "landline_phone_number": null,
                "address1": "221B Baker Street",
                "address2": null,
                "postcode": "NW16XE",
                "city": "London",
                "state": null,
                "country": "GB",
                "language": "en",
            },
            "shipping": {
                "title": "mr",
                "first_name": "John",
                "last_name": "Watson",
                "email": "john.watson@example.net",
                "mobile_phone_number": null,
                "landline_phone_number": null,
                "address1": "221B Baker Street",
                "address2": null,
                "postcode": "NW16XE",
                "city": "London",
                "state": null,
                "country": "GB",
                "language": "en",
                "delivery_type": "BILLING",
            },
            "hosted_payment": {
                "payment_url": "https://secure.payplug.com/pay/1FTGSRWYHla7eDkfTo2Usd",
                "return_url": "https://example.net/success?id=42",
                "cancel_url": "https://example.net/cancel?id=42",
            },
            "notification": {"url": "https://example.net/notifications?id=42"},
            "schedule": [
                {
                    "date": "2019-01-24",
                    "amount": 15000,
                    "payment_ids": ["pay_62VazeAbq5ttYietdC2QxR"],
                },
                {
                    "date": "2019-02-24",
                    "amount": 15000,
                    "payment_ids": ["pay_12uazeAbq5ttYietdC2QxP"],
                },
                {"date": "2019-03-24", "amount": 10000, "payment_ids": []},
            ],
            "failure": {
                "code": "a_failure_code",
                "message": 'A weird failure message ®±'
            },
            "metadata": {"customer_id": 42},
        }

        installment_plan_object = InstallmentPlan(**installment_plan_attributes)

        assert isinstance(installment_plan_object, InstallmentPlan)
        assert installment_plan_object.created_at == 1548326773
        assert installment_plan_object.currency == "EUR"
        assert installment_plan_object.is_fully_paid == False

        assert type(installment_plan_object.billing) == Payment.Billing
        assert installment_plan_object.billing.title == 'mr'
        assert installment_plan_object.billing.first_name == "John"
        assert installment_plan_object.billing.last_name == "Watson"
        assert installment_plan_object.billing.email == "john.watson@example.net"
        assert installment_plan_object.billing.address1 == '221B Baker Street'
        assert installment_plan_object.billing.postcode == 'NW16XE'
        assert installment_plan_object.billing.city == 'London'
        assert installment_plan_object.billing.country == 'GB'
        assert installment_plan_object.billing.language == 'en'
        
        assert type(installment_plan_object.shipping) == Payment.Shipping
        assert installment_plan_object.shipping.title == 'mr'
        assert installment_plan_object.shipping.first_name == "John"
        assert installment_plan_object.shipping.last_name == "Watson"
        assert installment_plan_object.shipping.email == "john.watson@example.net"
        assert installment_plan_object.shipping.address1 == '221B Baker Street'
        assert installment_plan_object.shipping.postcode == 'NW16XE'
        assert installment_plan_object.shipping.city == 'London'
        assert installment_plan_object.shipping.country == 'GB'
        assert installment_plan_object.shipping.language == 'en'
        assert installment_plan_object.shipping.delivery_type == 'BILLING'

        assert type(installment_plan_object.hosted_payment) == Payment.HostedPayment
        assert installment_plan_object.hosted_payment.payment_url == "https://secure.payplug.com/pay/1FTGSRWYHla7eDkfTo2Usd"
        assert installment_plan_object.hosted_payment.return_url == "https://example.net/success?id=42"
        assert installment_plan_object.hosted_payment.cancel_url == "https://example.net/cancel?id=42"


        assert installment_plan_object.notification.url == "https://example.net/notifications?id=42"
        assert type(installment_plan_object.schedule) == list
        for schedule in installment_plan_object.schedule:
            assert type(schedule) == InstallmentPlan.Schedule
            assert type(schedule.date) == str
            assert type(schedule.amount) == int
            assert type(schedule.payment_ids) == list
            for payment_id in schedule.payment_ids:
                assert type(payment_id) == str