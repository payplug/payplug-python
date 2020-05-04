# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'accounting_report_id'}, 201))
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: ({'id': 'accounting_report_id'}, 200))
class TestAccountingReportCreateRetrieve(TestBase):
    def test_retrieve(self):
        report = payplug.AccountingReport.retrieve('accounting_report_id')

        assert isinstance(report, resources.AccountingReport)
        assert report.id == 'accounting_report_id'

    def test_create(self):
        report = payplug.AccountingReport.create(some='report', da='ta')

        assert isinstance(report, resources.AccountingReport)
        assert report.id == 'accounting_report_id'
