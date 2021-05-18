# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase

@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'installment_plan_id'}, 200))
class TestInstallmentPlanRetrieve(TestBase):
    def test_retrieve(self):
        installment_plan = payplug.InstallmentPlan.retrieve('installment_plan_id')

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'