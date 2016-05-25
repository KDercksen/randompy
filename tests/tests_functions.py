#!/usr/bin/env python
# -*- coding: utf-8 -*-

import randompy.functions as f


class TestFunctions:

    def setup(self):
        self.resp = {
            'result': {
                'random': {
                    'data': 42,
                },
                'requestsLeft': 3,
                'advisoryDelay': 1000,
                'signature': 'result signature',
            },
            'error': {
                'code': -1,
                'message': 'Error with code -1',
                'data': 'Error data',
            }
        }

    def test_result_data(self):
        assert f.result_data(self.resp) == 42

    def test_result_obj(self):
        result = f.result_obj(self.resp)
        assert ('data', 42) in result.items()

    def test_result_all(self):
        result = f.result_all(self.resp)
        k = (key for key in self.resp['result'])
        assert all(key in k for key in result)

    def test_result_signature(self):
        assert f.result_signature(self.resp) == 'result signature'

    def test_result_advisory_delay(self):
        assert f.result_advisory_delay(self.resp) == 1000

    def test_result_requests_left(self):
        assert f.result_requests_left(self.resp) == 3

    def test_error_all(self):
        result = f.error_all(self.resp)
        k = (key for key in self.resp['error'])
        assert all(key in k for key in result)

    def test_error_message(self):
        assert f.error_message(self.resp) == 'Error with code -1'

    def test_error_code(self):
        assert f.error_code(self.resp) == -1

    def test_error_data(self):
        assert f.error_data(self.resp) == 'Error data'
