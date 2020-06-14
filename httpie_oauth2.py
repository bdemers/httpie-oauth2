"""
OAuth 2.0 Client Credentials Plugin for HTTPie.
"""
import sys
from httpie.plugins import AuthPlugin
from oauthlib.oauth2 import BackendApplicationClient, WebApplicationClient, InsecureTransportError
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth, AuthBase

from httpie.cli.definition import parser

from httpie.context import Environment

__version__ = '0.1.0'
__author__ = 'Brian Demers'
__licence__ = 'BSD'

class OAuth2Plugin(AuthPlugin):

    name = 'OAuth 2.0 Client Credentials'
    auth_type = 'oauth2'
    description = ''
    
    oauth = parser.add_argument_group(title='OAuth 2.0')

    oauth.add_argument(
        '--issuer-uri',
        default=None,
        metavar='ISSUER_URI',
        help="""
        The OAuth 2.0 Issuer URI
        """,
    )

    oauth.add_argument(
        '--scope',
        default=None,
        metavar='SCOPE',
        help="""
        The OAuth 2.0 Scopes
        """,
    )

    def get_auth(self, username, password):
        
        args = parser.args
        
        auth = HTTPBasicAuth(username, password)
        client = BackendApplicationClient(client_id=username)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=args.issuer_uri, auth=auth, scope=args.scope)

        return BearerAuth(token=token['access_token'])

class BearerAuth(AuthBase):
    """Adds proof of authorization (Bearer token) to the request."""

    def __init__(self, token):
        """Construct a new Bearer authorization object.
        :param token: bearer token to attach to request
        """
        self.token = token

    def __call__(self, r):
        """Append an Bearer header to the request.
        """
        r.headers['Authorization'] = 'Bearer %s' % self.token
        return r
