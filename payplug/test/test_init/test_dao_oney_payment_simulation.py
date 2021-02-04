# -*- coding: utf-8 -*-
from mock import patch
import payplug
from payplug import resources
from payplug.test import TestBase


@patch('payplug.config.secret_key', 'a_secret_key')
@patch.object(payplug.HttpClient, 'post', lambda *args, **kwargs: ({'id': 'simulation_id'}, 201))
class TestAccountingReportCreateRetrieve(TestBase):
    def test_retrieve(self):
        simulation = payplug.OneyPaymentSimulation.get_simulation(key='val')

        assert isinstance(simulation, resources.OneyPaymentSimulation)
        assert simulation.id == 'simulation_id'
