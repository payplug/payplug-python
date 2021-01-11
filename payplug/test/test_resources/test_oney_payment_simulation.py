# -*- coding: utf-8 -*-
from payplug.resources import OneyPaymentSimulation
from payplug.test import TestBase


class TestOneyPaymentSimulationResource(TestBase):
    def test_initializer_oney_payment_simulation(self):
        simulation_attributes = {
            "x3_with_fees": {
                "down_payment_amount": 67667,
                "nominal_annual_percentage_rate": 6.04,
                "effective_annual_percentage_rate": 6.21,
                "installments": [
                    {
                        "date": "2019-12-29T01:00:00.000Z",
                        "amount": 66667
                    },
                    {
                        "date": "2020-01-29T01:00:00.000Z",
                        "amount": 66666
                    }
                ],
                "total_cost": 1000
            },
        }

        simulation_object = OneyPaymentSimulation(**simulation_attributes)
        operation = simulation_object.x3_with_fees

        assert isinstance(operation, OneyPaymentSimulation.Operation)
        assert operation.down_payment_amount == 67667
        assert operation.nominal_annual_percentage_rate == 6.04
        assert operation.effective_annual_percentage_rate == 6.21
        assert operation.installments == [
            {
                "date": "2019-12-29T01:00:00.000Z",
                        "amount": 66667
            },
            {
                "date": "2020-01-29T01:00:00.000Z",
                        "amount": 66666
            }
        ]
        assert operation.total_cost == 1000
