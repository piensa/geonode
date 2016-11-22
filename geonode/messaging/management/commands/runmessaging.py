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

from django.core.management.base import BaseCommand
from optparse import make_option
import sys

from geonode.settings import BROKER_URL


class Command(BaseCommand):
    help = 'Start the MQ consumer to perform non blocking tasks'
    option_list = BaseCommand.option_list + (
        make_option(
            '-i',
            '--ignore-errors',
            action='store_true',
            dest='ignore_errors',
            default=False,
            help='Stop after any errors are encountered.'),
        )

    def handle(self, **options):
        ignore_errors = options.get('ignore_errors')
        verbosity = int(options.get('verbosity'))

        if verbosity > 0:
            console = sys.stdout
            print "Verbosity is", verbosity
        else:
            console = None

        from kombu import BrokerConnection
        from geonode.messaging.consumer import Consumer

        with BrokerConnection(BROKER_URL) as connection:
            try:
                print ("Consumer starting.")
                worker = Consumer(connection)
                worker.run()
            except KeyboardInterrupt:
                print ("Consumer stopped.")