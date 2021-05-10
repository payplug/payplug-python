# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase

@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({"some":"installment_plan", "da":"ta"}, 201))
@patch.object(payplug.HttpClient, 'patch', lambda *args, **kwargs: ({'id': 'installment_plan_id'}, 200))
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'installment_plan_id'}, 200))
class TestInstallmentPlanRetrieve(TestBase):
    def test_get(self):
        installment_plan = payplug.InstallmentPlan.get('installment_plan_id')

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'

    def test_update(self):
        installment_plan = payplug.InstallmentPlan.get('installment_plan_id')
        installment_plan = payplug.InstallmentPlan.update(installment_plan)

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'
    
    def test_create(self):
        installment_plan = payplug.InstallmentPlan.create()

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.some == 'installment_plan'