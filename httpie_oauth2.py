"""
OAuth 2.0 Client Credentials Plugin for HTTPie.
Extended to support "resource" parameter too, required for ADFS 2016/2019 OAuth2 `client_credential` flows
"""
from httpie.plugins import AuthPlugin
from oauthlib.oauth2 import BackendApplicationClient, OAuth2Error
from requests_oauthlib import OAuth2Session
from requests.auth import AuthBase

from httpie.cli.definition import parser

__version__ = '0.1.1'
__author__ = 'Brian Demers'
__licence__ = 'BSD'

class HttpieOAuth2Error(Exception):
    """HTTPie OAuth2 Auth-Plugin Error.

    Raised if the OAuth2 token request is missing or invalid.
    """
    pass

class OAuth2Plugin(AuthPlugin):

    name = 'OAuth 2.0 Client Credentials'
    auth_type = 'oauth2'
    description = ''
    
    oauth = parser.add_argument_group(title='OAuth 2.0')

    oauth.add_argument(
        '--token-url',
        default=None,
        metavar='TOKEN_URL',
        help="""
        The OAuth 2.0 Token URL
        """,
    )

    oauth.add_argument(
        '--scope',
        default='user_impersonation', # predefine default scope
        metavar='SCOPE',
        help="""
        The OAuth 2.0 Scopes
        """,
    )

    # 210507 pa: adding support for optional "resource"  parameter, required for ADFS 2016/2019 OAuth2 
    oauth.add_argument(
        '--resource',
        default=None,
        metavar='RESOURCE',
        help="""
        The OAuth 2.0 Resource (required for ADFS 2016/2019 OAuth2)
        """,
    )

    def get_auth(self, username, password):
        
        args = parser.args
        client_id, client_secret = username, password
        custom_args = {}
        if args.resource:
            custom_args['resource'] = args.resource

        try:
            client = BackendApplicationClient(client_id=client_id)
            oauth = OAuth2Session(client=client)
            # print('---# new token requested #---')
            token_result = oauth.fetch_token(
                token_url=args.token_url, 
                client_id=client_id,
                client_secret=client_secret,
                scope=args.scope,
                **custom_args,
                )
        except OAuth2Error as oauth_error:
            raise HttpieOAuth2Error(
                "Error generating access token: {0}, {1}, {2}".format(
                    oauth_error.error, oauth_error.status_code, oauth_error.description
                )
            )
        else:                
            return BearerAuth(token=token_result.get('access_token'))

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
