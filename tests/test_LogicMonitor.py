#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

import fake
import mock
from logicmonitor_core.LogicMonitor import LogicMonitor
from should import it


class TestLogicMonitor_rpc(unittest.TestCase):

    """ test cases for LogicMonitor.rpc """

    def setUp(self):
        fake.FakeLogicMonitor.clear()

        self.lm = LogicMonitor(None, **{
            "company": "Comp",
            "user": "admin",
            "password": "admin"
        })
        self.mocked_json = {
            "auth_failed": fake.FakeLogicMonitor.AUTH_ERROR,
            "succ": fake.FakeLogicMonitor.GET_HOST_GROUP_SUCC
        }

    def tearDown(self):
        pass

    @mock.patch("urllib2.urlopen")
    def test_request_success(self, mocked_urlopen):
        pass

    @mock.patch("sys.exit")
    @mock.patch("urllib2.urlopen")
    def test_request_failed_with_ioerror(self, mocked_urlopen, mocked_exit):
        mocked_urlopen.side_effect = IOError
        self.lm.rpc('test', {'a': 1, 'b': 2})
        mocked_exit.assert_called_with(1)

    @mock.patch("sys.exit")
    @mock.patch("urllib2.urlopen")
    def test_request_failed_with_auth(self, mocked_urlopen, mocked_exit):
        mocked_urlopen.return_value = fake.FakeLogicMonitor.AUTH_ERROR
        self.lm.rpc("test", {"a": 1, "b": 3})
        mocked_exit.assert_called_with(1)


class TestLogicMonitor_get_group(unittest.TestCase):

    """ test cases for LogicMonitor.getgroup """

    @mock.patch("urllib2.urlopen")
    def setUp(self, mocked_urlopen):

        fake.FakeLogicMonitor.clear()

        self.lm = LogicMonitor(None, **{
            "company": "MockComp",
            "user": "MockUser",
            "password": "MockPwd",
        })
        self.urlopen = mocked_urlopen

    def tearDown(self):
        pass

    def test_get_group_with_exists_group(self):
        mocked_json = fake.FakeLogicMonitor.GET_HOST_GROUP_SUCC
        self.urlopen.return_value = mocked_json

        group = self.lm.get_group("MockGroup")

        it(group).should.be.dict

    def test_get_group_with_non_exists_group(self):
        mocked_json = fake.FakeLogicMonitor.GET_HOST_GROUP_FAILED
        self.urlopen.return_value = mocked_json

        group = self.lm.get_group("Non-MockGroup")

        it(group).should.be.none

    def test_get_group_with_failed_request(self):
        mocked_json = fake.FakeLogicMonitor.GET_HOST_GROUP_FAILED
        self.urlopen.return_value = mocked_json

        group = self.lm.get_group("Non-MockGroup")

        it(group).should.be.none
