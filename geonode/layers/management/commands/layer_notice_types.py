# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import notification

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_noop as _

class Command(BaseCommand):
    help = ("Create notice types for layers")

    def handle(self, *args, **options):
        notification.models.NoticeType.create(
            "layer_created",
            _("Layer Created"),
            _("A Layer was created"))
        notification.models.NoticeType.create(
            "layer_updated",
            _("Layer Updated"),
            _("A Layer was updated"))
        notification.models.NoticeType.create(
            "layer_deleted",
            _("Layer Deleted"),
            _("A Layer was deleted"))
        notification.models.NoticeType.create(
            "layer_comment",
            _("Comment on Layer"),
            _("A layer was commented on"))
        notification.models.NoticeType.create(
            "layer_rated",
            _("Rating for Layer"),
            _("A rating was given to a layer"))
        notification.models.NoticeType.create(
            "request_download_resourcebase",
            _("Request download to an owner"),
            _("A request has been sent to the owner"))