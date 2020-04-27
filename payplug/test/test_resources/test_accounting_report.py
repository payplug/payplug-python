# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug.resources import AccountingReport
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
class TestAccountingReportResource(TestBase):
    def test_initialize_accounting_report(self):
        report_attributes = {
            'start_date': '2020-01-01',
            'object': 'accounting_report',
            'notification_url': 'notification_url',
            'end_date': '2020-04-30',
            'id': 'ar_1GKEACvltTVXT5muBd3AQv',
            'file_available_until': 1588083743,
            'temporary_url': 'temporary_url'
        }

        report_object = AccountingReport(**report_attributes)

        assert report_object.id == 'ar_1GKEACvltTVXT5muBd3AQv'
        assert report_object.start_date == '2020-01-01'
        assert report_object.end_date == '2020-04-30'
        assert report_object.notification_url == 'notification_url'
        assert report_object.file_available_until == 1588083743
        assert report_object.temporary_url == 'temporary_url'


def report_fixture():
    return {
        "id": "ar_1GKEACvltTVXT5muBd3AQv",
        "object": "accounting_report",
    }


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'get', lambda *args, **kwargs: (report_fixture(), 200))
class TestConsistentAccountingReport(TestBase):
    @patch('payplug.resources.routes.url')
    def test_get_consistent_resource(self, routes_url_mock):
        unsafe_report = AccountingReport(id='ar_1GKEACvltTVXT5muBd3AQv_unsafe',
                                         object='accounting_report')
        safe_report = unsafe_report.get_consistent_resource()

        assert isinstance(safe_report, AccountingReport)
        assert routes_url_mock.call_args[1]['resource_id'] == 'ar_1GKEACvltTVXT5muBd3AQv_unsafe'
        assert safe_report.id == 'ar_1GKEACvltTVXT5muBd3AQv'
