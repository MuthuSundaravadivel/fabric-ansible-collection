#!/usr/bin/python
#
# SPDX-License-Identifier: Apache-2.0
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import base64
import json

from .certificate_authorities import CertificateAuthority
from .consoles import Console
from .enrolled_identities import EnrolledIdentity
from .ordering_services import OrderingService, OrderingServiceNode
from .organizations import Organization
from .peers import Peer
from .cert_utils import split_ca_chain


def get_console(module):

    # Log in to the console.
    api_endpoint = module.params['api_endpoint']
    api_authtype = module.params['api_authtype']
    api_key = module.params['api_key']
    api_secret = module.params['api_secret']
    api_timeout = module.params['api_timeout']
    api_token_endpoint = module.params['api_token_endpoint']
    console = Console(module, api_endpoint, api_timeout, api_token_endpoint)
    console.login(api_authtype, api_key, api_secret)
    if console.is_v1():
        module.warn('Console only supports v1 APIs, only limited functionality will be available')
    return console


def get_certificate_authority_by_name(console, name, fail_on_missing=True):

    # Look up the certificate authority by name.
    component = console.get_component_by_display_name('fabric-ca', name)
    if component is None:
        if fail_on_missing:
            raise Exception(f'The certificate authority {name} does not exist')
        else:
            return None
    data = console.extract_ca_info(component)
    return CertificateAuthority.from_json(data)


def get_certificate_authority_by_module(console, module, parameter_name='certificate_authority'):

    # If the certificate authority is a dictionary, then we assume that
    # it contains all of the required keys/values.
    certificate_authority = module.params[parameter_name]
    if isinstance(certificate_authority, dict):
        return CertificateAuthority.from_json(certificate_authority)

    # Otherwise, it is the display name of a certificate authority that
    # we need to look up.
    component = console.get_component_by_display_name('fabric-ca', certificate_authority)
    if component is None:
        raise Exception(f'The certificate authority {certificate_authority} does not exist')
    data = console.extract_ca_info(component)

    # Return the certificate authority.
    return CertificateAuthority.from_json(data)


def get_all_certificate_authorities(console):

    # Go over each peer.
    certificate_authorities = list()

    components = console.get_all_components_by_type('fabric-ca')
    if len(components) == 0:
        return None

    for component in components:

        data = console.extract_ca_info(component)

        # Add the peer.
        certificate_authorities.append(CertificateAuthority.from_json(data))

    # Return the list of peers.
    return certificate_authorities


def get_organization_by_name(console, name, fail_on_missing=True):

    # Look up the organization by name.
    component = console.get_component_by_display_name('msp', name)
    if component is None:
        if fail_on_missing:
            raise Exception(f'The organization {name} does not exist')
        else:
            return None
    data = console.extract_organization_info(component)
    return Organization.from_json(data)


def get_organization_by_module(console, module, parameter_name='organization'):

    # If the organization is a dict, then we assume that
    # it contains all of the required keys/values.
    organization = module.params[parameter_name]
    if isinstance(organization, dict):
        return Organization.from_json(organization)

    # Otherwise, it is the display name of an organization that
    # we need to look up.
    component = console.get_component_by_display_name('msp', organization)
    if component is None:
        raise Exception(f'The organization {organization} does not exist')
    data = console.extract_organization_info(component)

    # Return the organization.
    return Organization.from_json(data)


def get_organizations_by_module(console, module, parameter_name='organizations'):

    # Go over each organization.
    organizations = list()
    for organization in module.params[parameter_name]:

        # If the organization is a dict, then we assume that
        # it contains all of the required keys/values.
        if isinstance(organization, dict):
            organizations.append(Organization.from_json(organization))
            continue

        # Otherwise, it is the display name of an organization that
        # we need to look up.
        component = console.get_component_by_display_name('msp', organization)
        if component is None:
            raise Exception(f'The organization {organization} does not exist')
        data = console.extract_organization_info(component)

        # Add the organization.
        organizations.append(Organization.from_json(data))

    # Return the list of organizations.
    return organizations


def get_peer_by_name(console, name, fail_on_missing=True):

    # Look up the peer by name.
    component = console.get_component_by_display_name('fabric-peer', name)
    if component is None:
        if fail_on_missing:
            raise Exception(f'The peer {name} does not exist')
        else:
            return None
    data = console.extract_peer_info(component)
    return Peer.from_json(data)


def get_peer_by_module(console, module, parameter_name='peer'):

    # If the peer is a dict, then we assume that
    # it contains all of the required keys/values.
    peer = module.params[parameter_name]
    if isinstance(peer, dict):
        return Peer.from_json(peer)

    # Otherwise, it is the display name of a peer that
    # we need to look up.
    component = console.get_component_by_display_name('fabric-peer', peer)
    if component is None:
        raise Exception(f'The peer {peer} does not exist')
    data = console.extract_peer_info(component)

    # Return the peer.
    return Peer.from_json(data)


def get_peers_by_module(console, module, parameter_name='peers'):

    # Go over each peer.
    peers = list()
    for peer in module.params[parameter_name]:

        # If the peer is a dict, then we assume that
        # it contains all of the required keys/values.
        if isinstance(peer, dict):
            peers.append(Peer.from_json(peer))
            continue

        # Otherwise, it is the display name of an peer that
        # we need to look up.
        component = console.get_component_by_display_name('fabric-peer', peer)
        if component is None:
            raise Exception(f'The peer {peer} does not exist')
        data = console.extract_peer_info(component)

        # Add the peer.
        peers.append(Peer.from_json(data))

    # Return the list of organizations.
    return peers


def get_all_peers(console):

    # Go over each peer.
    peers = list()

    components = console.get_all_components_by_type('fabric-peer')
    if len(components) == 0:
        return None

    for component in components:

        data = console.extract_peer_info(component)

        # Add the peer.
        peers.append(Peer.from_json(data))

    # Return the list of peers.
    return peers


def get_all_orderering_service_nodes(console):

    # Go over each peer.
    ordering_service_nodes = list()

    components = console.get_all_components_by_type('fabric-orderer')
    if len(components) == 0:
        return None

    for component in components:

        data = console.extract_ordering_service_node_info(component)

        # Add the ordering service node.
        ordering_service_nodes.append(OrderingServiceNode.from_json(data))

    # Return the list of ordering service nodes.
    return ordering_service_nodes


def get_all_organizations(console):

    # Go over each peer.
    organizations = list()

    components = console.get_all_components_by_type('msp')

    if len(components) == 0:
        return None

    for component in components:

        data = console.extract_organization_info(component)

        # Add the ordering service node.
        organizations.append(Organization.from_json(data))

    # Return the list of ordering service nodes.
    return organizations


def get_ordering_service_by_name(console, name, fail_on_missing=True):

    # Look up the ordering service by name.
    components = console.get_components_by_cluster_name('fabric-orderer', name)
    if len(components) == 0:
        if fail_on_missing:
            raise Exception(f'The ordering service {name} does not exist')
        else:
            return None
    data = console.extract_ordering_service_info(components)
    return OrderingService.from_json(data)


def get_ordering_service_by_module(console, module, parameter_name='ordering_service'):

    # If the ordering service is a list, then we assume that
    # it contains all of the required keys/values.
    ordering_service = module.params[parameter_name]
    if isinstance(ordering_service, list):
        return OrderingService.from_json(ordering_service)

    # Otherwise, it is the display name of a ordering service that
    # we need to look up.
    components = console.get_components_by_cluster_name('fabric-orderer', ordering_service)
    if len(components) == 0:
        raise Exception(f'The ordering service {ordering_service} does not exist')
    data = console.extract_ordering_service_info(components)

    # Return the ordering service.
    return OrderingService.from_json(data)


def get_ordering_service_node_by_name(console, name, fail_on_missing=True):

    # Look up the ordering service node by name.
    component = console.get_component_by_display_name('fabric-orderer', name)
    if component is None:
        if fail_on_missing:
            raise Exception(f'The peer {name} does not exist')
        else:
            return None
    data = console.extract_ordering_service_node_info(component)
    return OrderingServiceNode.from_json(data)


def get_ordering_service_node_by_module(console, module, parameter_name='ordering_service_node'):

    # If the ordering service is a list, then we assume that
    # it contains all of the required keys/values.
    ordering_service_node = module.params[parameter_name]
    if isinstance(ordering_service_node, dict):
        return OrderingServiceNode.from_json(ordering_service_node)

    # Otherwise, it is the display name of a ordering service that
    # we need to look up.
    component = console.get_component_by_display_name('fabric-orderer', ordering_service_node)
    if component is None:
        raise Exception(f'The ordering service node {ordering_service_node} does not exist')
    data = console.extract_ordering_service_node_info(component)

    # Return the ordering service.
    return OrderingServiceNode.from_json(data)


def get_ordering_service_nodes_by_module(console, module, parameter_name='ordering_service_nodes'):

    # Go over each ordering service node.
    ordering_service_nodes = list()
    for ordering_service_node in module.params[parameter_name]:

        # If the ordering service node is a dict, then we assume that
        # it contains all of the required keys/values.
        if isinstance(ordering_service_node, dict):
            ordering_service_nodes.append(OrderingServiceNode.from_json(ordering_service_node))
            continue

        # Otherwise, it is the display name of an ordering service node
        # that we need to look up.
        component = console.get_component_by_display_name('fabric-orderer', ordering_service_node)
        if component is None:
            raise Exception(f'The ordering service node {ordering_service_node} does not exist')
        data = console.extract_ordering_service_node_info(component)

        # Add the ordering service node.
        ordering_service_nodes.append(OrderingServiceNode.from_json(data))

    # Return the list of ordering service nodes.
    return ordering_service_nodes


def get_certs_from_certificate_authority(console, module):

    # Get the certificate authority.
    if module.params['certificate_authority'] is None:
        return None
    certificate_authority = get_certificate_authority_by_module(console, module)

    # Get the certificate authority information.
    with certificate_authority.connect(module, None) as connection:
        ca_chain = connection.get_ca_chain()
        tlsca_chain = connection.get_tlsca_chain()

    # Split the certificate authority chains into root certificates and intermediate certificates.
    (root_certs, intermediate_certs) = split_ca_chain(ca_chain)
    (tls_root_certs, tls_intermediate_certs) = split_ca_chain(tlsca_chain)

    # Build the return information.
    result = {
        'root_certs': root_certs,
        'intermediate_certs': intermediate_certs,
        'tls_root_certs': tls_root_certs,
        'tls_intermediate_certs': tls_intermediate_certs
    }

    # Generate a revocation list if a registrar has been provided.
    if module.params['registrar']:
        registrar = get_identity_by_module(module, 'registrar')
        hsm = module.params['hsm']
        with certificate_authority.connect(module, hsm) as connection:
            revocation_list = connection.generate_crl(registrar)
            result['revocation_list'] = [revocation_list]

    # Return the information retrieved from the certificate authority.
    return result


def get_identity_by_module(module, parameter_name='identity'):

    # If the identity is a dictionary, then we assume that
    # it contains all of the required keys/values.
    identity = module.params[parameter_name]
    if isinstance(identity, dict):
        return EnrolledIdentity.from_json(identity)

    # Otherwise, it is the file name of a identity that
    # we need to read.
    with open(identity, 'r') as file:
        data = json.load(file)
    return EnrolledIdentity.from_json(data)


def resolve_identity(console, module, identity, msp_id):

    # If the identity contains the CA field, then we do
    # not need to resolve it.
    if identity.ca is not None:
        return identity

    # If a console instance has not been provided, we
    # need one for the following operation.
    if not console:
        if not module.params['api_endpoint']:
            raise Exception('Specified identity does not contain a CA field, and no console details provided')
        console = get_console(module)

    # The identity does not contain the CA field, so we
    # need to ask the console for the organization that
    # matches the specified MSP ID, and then extract the
    # CA field from that.
    msps = console.get_msps_by_msp_id(msp_id)
    if not msps:
        raise Exception(f'Specified identity does not contain a CA field, and cannot find CA certificates for MSP ID {msp_id}')
    all_root_certs = []
    all_intermediate_certs = []
    for msp in msps:
        root_certs = msp.get('root_certs', list())
        intermediate_certs = msp.get('intermediate_certs', list())
        all_root_certs.extend(root_certs)
        all_intermediate_certs.extend(intermediate_certs)
    all_certs = all_root_certs + all_intermediate_certs
    parsed_certs = []
    for cert in all_certs:
        parsed_certs.append(base64.b64decode(cert).decode('utf8'))
    identity.ca = "\n".join(parsed_certs).encode('utf8')
    return identity
