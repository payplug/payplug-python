# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase

@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'installment_plan_id'}, 200))
@patch.object(payplug.HttpClient, 'patch', lambda *args, **kwargs: ({'id': 'installment_plan_id', 'failure': {'code': 'aborted'}}, 204))
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'installment_plan_id'}, 201))
class TestInstallmentPlanRetrieve(TestBase):
    def test_retrieve(self):
        installment_plan = payplug.InstallmentPlan.retrieve('installment_plan_id')

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'


    def test_update(self):
        installment_plan = payplug.InstallmentPlan.retrieve('installment_plan_id')
        installment_plan = payplug.InstallmentPlan.abort(installment_plan)

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'
        assert installment_plan.failure['code'] == 'aborted'


    def test_create(self):
        installment_plan = payplug.InstallmentPlan.create()

        assert isinstance(installment_plan, resources.InstallmentPlan)
        assert installment_plan.id == 'installment_plan_id'
    