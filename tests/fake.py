#!/usr/bin/env python
# -*- coding: utf-8 -*-


GET_HOST_GROUP_SUCC_JSON = {
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
}

GET_HOST_GROUP_FAILED_JSON = {
    "errmsg": "internal server error",
    "status": 500,
}
