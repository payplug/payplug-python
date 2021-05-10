from payplug.resources import InstallmentPlan
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
            "failure": null,
            "metadata": {"customer_id": 42},
        }

        installment_plan_object = InstallmentPlan(**installment_plan_attributes)
        
        assert isinstance(installment_plan_object, InstallmentPlan)
        assert installment_plan_object.created_at == 1548326773
        assert installment_plan_object.currency == "EUR"
        assert installment_plan_object.billing == {
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
            }
        assert installment_plan_object.shipping == {
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
            }
