#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apistar import http, annotate

from auth import IsAuthenticated, BasicAuthentication
from models.typesystems import SpiderData
from models.models import Crate


@annotate(
    authentication=[BasicAuthentication()],
    permissions=[IsAuthenticated()]
)
def callback(data: SpiderData):
    for crate_data in data:
        Crate.create(pk=crate_data['id'], crate=crate_data)

    return http.Response({}, status=201)
