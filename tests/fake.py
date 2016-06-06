#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json


def dump_to_StringIO(json_relative):
    """ dump a json relative object to a StringIO

    :type json: mixed
    :returns: unicode

    """
    return io.StringIO(unicode(json.dumps(json_relative)))


class FakeJSONs(object):

    """ mocked jsons.
    You need to call .clear() to ensure the contents in the setup() """

    @classmethod
    def clear(cls):
        """ clear all read history """
        for name in dir(cls):
            item = getattr(cls, name)
            if isinstance(item, io.StringIO):
                item.seek(0)


class FakeLogicMonitor(FakeJSONs):

    AUTH_ERROR = dump_to_StringIO({
            "errmsg": "anything",
            "status": 403,
            })

    GET_HOST_GROUP_SUCC = dump_to_StringIO({
        "errmsg": "OK",
        "status": 200,
        "data": [
            {"fullPath": "MockGroup",
             "groupType": "0",
             "extra": "",
             "name": "MockGroup",
             "description": "",
             "alertEnable": True,
             "appliesTo": "",
             "id": 2,
             "createOn": 1428654576,
             "parentId": 1
             }
        ]
    })

    GET_HOST_GROUP_FAILED = dump_to_StringIO({
        "errmsg": "internal server error",
        "status": 500,
    })
