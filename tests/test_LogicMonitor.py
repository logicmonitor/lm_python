#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import json
import unittest

import mock
from should import it

from logicmonitor_core.LogicMonitor import LogicMonitor
import fake



class TestLogicMonitor_get_group(unittest.TestCase):

    """ test cases for LogicMonitor """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("urllib2.urlopen")
    def test_get_group_with_exists_group(self, mocked_url_open):
        mocked_json = io.StringIO(
            unicode(json.dumps(fake.GET_HOST_GROUP_SUCC_JSON)))
        mocked_url_open.return_value = mocked_json

        self.lm = LogicMonitor(None, **{
            "company": "MockComp",
            "user": "MockUser",
            "password": "MockPwd",
        })

        group = self.lm.get_group("MockGroup")

        it(group).should.be.dict

    @mock.patch("urllib2.urlopen")
    def test_get_group_with_non_exists_group(self, mocked_url_open):
        mocked_json = io.StringIO(
            unicode(json.dumps(fake.GET_HOST_GROUP_SUCC_JSON)))
        mocked_url_open.return_value = mocked_json

        self.lm = LogicMonitor(None, **{
            "company": "MockComp",
            "user": "MockUser",
            "password": "MockPwd",
        })

        group = self.lm.get_group("Non-MockGroup")

        it(group).should.be.none

    @mock.patch("urllib2.urlopen")
    def test_get_group_with_failed_request(self, mocked_url_open):
        mocked_json = io.StringIO(
            unicode(json.dumps(fake.GET_HOST_GROUP_FAILED_JSON)))
        mocked_url_open.return_value = mocked_json

        self.lm = LogicMonitor(None, **{
            "company": "MockComp",
            "user": "MockUser",
            "password": "MockPwd",
        })

        group = self.lm.get_group("Non-MockGroup")

        it(group).should.be.none
