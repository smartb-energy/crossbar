#####################################################################################
#
#  Copyright (c) Crossbar.io Technologies GmbH
#
#  Unless a separate license agreement exists between you and Crossbar.io GmbH (e.g.
#  you have purchased a commercial license), the license terms below apply.
#
#  Should you enter into a separate license agreement after having received a copy of
#  this software, then the terms of such license agreement replace the terms below at
#  the time at which such license agreement becomes effective.
#
#  In case a separate license agreement ends, and such agreement ends without being
#  replaced by another separate license agreement, the license terms below apply
#  from the time at which said agreement ends.
#
#  LICENSE TERMS
#
#  This program is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License, version 3, as published by the
#  Free Software Foundation. This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU Affero General Public License Version 3 for more details.
#
#  You should have received a copy of the GNU Affero General Public license along
#  with this program. If not, see <http://www.gnu.org/licenses/agpl-3.0.en.html>.
#
#####################################################################################

from __future__ import absolute_import

import time

import txaio

import crossbar
from crossbar.common import checkconfig
from crossbar.controller.processtypes import RouterWorkerProcess, ContainerWorkerProcess, WebSocketTesteeWorkerProcess
from crossbar.worker.transport.factory import create_router_transport
from crossbar.worker.transport.resource import create_web_service, add_web_services, remove_web_services
from crossbar.controller.node import Node
from crossbar.worker.router import RouterWorkerSession
from crossbar.worker.container import ContainerWorkerSession
from crossbar.worker.testee import WebSocketTesteeWorkerSession


def default_native_workers():
    factory = dict()
    factory['router'] = {
        'class': RouterWorkerProcess,
        'worker_class': RouterWorkerSession,

        # check a whole router worker configuration item (including realms, transports, ..)
        'checkconfig_item': checkconfig.check_router,

        # only check router worker options
        'checkconfig_options': checkconfig.check_router_options,

        'logname': 'Router',
        'topics': {
            'starting': u'crossbar.node.on_router_starting',
            'started': u'crossbar.node.on_router_started',
        }
    }
    factory['container'] = {
        'class': ContainerWorkerProcess,
        'worker_class': ContainerWorkerSession,

        # check a whole container worker configuration item (including components, ..)
        'checkconfig_item': checkconfig.check_container,

        # only check container worker options
        'checkconfig_options': checkconfig.check_container_options,

        'logname': 'Container',
        'topics': {
            'starting': u'crossbar.node.on_container_starting',
            'started': u'crossbar.node.on_container_started',
        }
    }
    factory['websocket-testee'] = {
        'class': WebSocketTesteeWorkerProcess,
        'worker_class': WebSocketTesteeWorkerSession,

        # check a whole websocket testee worker configuration item
        'checkconfig_item': checkconfig.check_websocket_testee,

        # only check websocket testee worker worker options
        'checkconfig_options': checkconfig.check_websocket_testee_options,

        'logname': 'WebSocketTestee',
        'topics': {
            'starting': u'crossbar.node.on_websocket_testee_starting',
            'started': u'crossbar.node.on_websocket_testee_started',
        }
    }
    return factory


_TITLE = "Crossbar.io Standalone"

# http://patorjk.com/software/taag/#p=display&h=1&f=Stick%20Letters&t=Crossbar.io
_BANNER = r"""     __  __  __  __  __  __      __
    /  `|__)/  \/__`/__`|__) /\ |__)
    \__,|  \\__/.__/.__/|__)/~~\|  \

    {} {}, https://crossbar.io
    Copyright (c) 2013-{} Crossbar.io Technologies GmbH, open-source licensed under AGPL 3.0.
"""


class Personality(object):
    """
    Software personality for Crossbar.io OSS.

    This is a policy class that configures various parts of Crossbar.io's
    behavior.
    """

    log = txaio.make_logger()

    NAME = 'standalone'

    TITLE = _TITLE

    DESC = crossbar.__doc__

    BANNER = _BANNER.format(_TITLE, crossbar.__version__, time.strftime('%Y'))

    LEGAL = ('crossbar', 'LEGAL')

    # a list of directories to serach Jinja2 templates for
    # rendering various web resources. this must be a list
    # of _pairs_ to be used with pkg_resources.resource_filename()!
    TEMPLATE_DIRS = [('crossbar', 'web/templates')]

    NodeKlass = Node

    WorkerKlasses = [RouterWorkerSession, ContainerWorkerSession, WebSocketTesteeWorkerSession]

    native_workers = default_native_workers()

    create_router_transport = create_router_transport
    """
    Create a router (listening) transport from a (complete) router transport configuration:

        (reactor, name, config, cbdir, log, node,
         _router_session_factory=None, _web_templates=None, add_paths=False) -> None
    """

    create_web_service = create_web_service
    """
    Create a (single) Web service to be added to a Web service tree:

        (reactor, path_config, templates, log, cbdir, _router_session_factory, node, nested=True) -> None
    """

    add_web_services = add_web_services
    """
    Add Web service(s) to a Web service tree:

        (reactor, resource, paths, templates, log, cbdir, _router_session_factory, node) -> None
    """

    remove_web_services = remove_web_services
    """
    Remove web service(s) from a Web service tree:

        (reactor, resource, paths) -> None
    """

    #
    # configuration related functions
    #

    # config
    check_config = checkconfig.check_config

    # config files
    upgrade_config_file = checkconfig.upgrade_config_file
    convert_config_file = checkconfig.convert_config_file
    check_config_file = checkconfig.check_config_file

    # top level
    check_controller = checkconfig.check_controller
    check_controller_options = checkconfig.check_controller_options
    check_worker = checkconfig.check_worker

    # native workers
    check_manhole = checkconfig.check_manhole
    check_connection = checkconfig.check_connection

    # router worker
    check_router = checkconfig.check_router
    check_router_options = checkconfig.check_router_options
    check_router_realm = checkconfig.check_router_realm
    check_router_realm_role = checkconfig.check_router_realm_role
    check_router_component = checkconfig.check_router_component

    # container worker
    check_container = checkconfig.check_container
    check_container_options = checkconfig.check_container_options
    check_container_component = checkconfig.check_container_component

    # guest worker
    check_guest = checkconfig.check_guest

    # testee worker
    check_websocket_testee = checkconfig.check_websocket_testee
    check_websocket_testee_options = checkconfig.check_websocket_testee_options

    # listening transports
    check_router_transport = checkconfig.check_router_transport
    check_listening_endpoint = checkconfig.check_listening_endpoint
    check_listening_transport_universal = checkconfig.check_listening_transport_universal
    check_listening_transport_websocket = checkconfig.check_listening_transport_websocket
    check_listening_transport_web = checkconfig.check_listening_transport_web

    # web services
    check_paths = checkconfig.check_paths
    check_web_path_service = checkconfig.check_web_path_service

    # authentication
    check_transport_auth = checkconfig.check_transport_auth
    check_transport_cookie = checkconfig.check_transport_cookie

    # connecting transports
    check_connecting_endpoint = checkconfig.check_connecting_endpoint
    check_connecting_transport = checkconfig.check_connecting_transport

    # check_listening_transport_websocket = checkconfig.check_listening_transport_websocket
    check_listening_transport_rawsocket = checkconfig.check_listening_transport_rawsocket
    # check_listening_transport_universal = checkconfig.check_listening_transport_universal
    # check_listening_transport_web = checkconfig.check_listening_transport_web
    check_listening_transport_mqtt = checkconfig.check_listening_transport_mqtt
    check_listening_transport_flashpolicy = checkconfig.check_listening_transport_flashpolicy
    check_listening_transport_websocket_testee = checkconfig.check_listening_transport_websocket_testee
    check_listening_transport_stream_testee = checkconfig.check_listening_transport_stream_testee

    check_listening_endpoint_onion = checkconfig.check_listening_endpoint_onion
