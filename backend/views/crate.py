#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apistar import annotate, render_template
from apistar.renderers import HTMLRenderer

from models.models import Crate


@annotate(renderers=[HTMLRenderer()])
def crate_list():
    crates = Crate.all()
    return render_template('home.html', crates=crates)


@annotate(renderers=[HTMLRenderer()])
def crate_detail(crate_id: int):
    template = "404.html"
    crate = Crate.get(pk=crate_id)
    if crate:
        template = "detail.html"
    return render_template(template, crate=crate)
