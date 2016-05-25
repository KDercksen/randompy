#!/usr/bin/env python
# -*- coding: utf-8 -*-


def result_data(resp):
    return resp['result']['random']['data']


def result_obj(resp):
    return resp['result']['random']


def result_all(resp):
    return resp['result']


def result_signature(resp):
    return resp['result']['signature']


def result_advisory_delay(resp):
    return resp['result']['advisoryDelay']


def result_requests_left(resp):
    return resp['result']['requestsLeft']


def error_all(resp):
    return resp['error']


def error_message(resp):
    return resp['error']['message']


def error_code(resp):
    return resp['error']['code']


def error_data(resp):
    return resp['error']['data']
