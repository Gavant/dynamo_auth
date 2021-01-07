import time
from authlib.oauth2.rfc6750 import InvalidTokenError
from flywheel import Engine
from .models import OAuth2DynamoToken, OAuth2DynamoClient
# from flywheel import Engine
# from flywheel import Model, Field, STRING, NUMBER

#for client
# from werkzeug.utils import cached_property
# from authlib.common.encoding import json_loads, json_dumps
# from authlib.oauth2.rfc6749 import ClientMixin

# from authlib.oauth2.rfc6749.util import scope_to_list, list_to_scope


# class OAuth2DynamoToken(Model):
#     client_id = Field(type=STRING)
#     user_id = Field(type=NUMBER)
#     token_type = Field(type=STRING)
#     access_token = Field(hash_key=True)
#     refresh_token = Field(type=STRING)
#     scope = Field()
#     revoked = Field(type=bool)
#     issued_at = Field(type=NUMBER)
#     expires_in = Field(type=NUMBER)

#     def get_client_id(self):
#         return self.client_id

#     def get_scope(self):
#         return self.scope

#     def get_expires_in(self):
#         return self.expires_in

#     def get_expires_at(self):
#         return self.issued_at + self.expires_in

#     def is_refresh_token_active(self):
#         if self.revoked:
#             return False
#         expires_at = self.issued_at + self.expires_in * 2
#         return expires_at >= time.time()


class Dynamo():
    engine = Engine()

    def init_engine(self, dy_region, use_local, local_port=8000, create_tables=False):
        # Create an engine and connect to an AWS region
        if use_local:
            self.engine.connect(host='localhost', port=local_port, region='us-east-1', is_secure=False)
        else:
            self.engine.connect(region=dy_region, is_secure=False)

        # Register our models with the engine so it can create the Dynamo table
        self.engine.register(OAuth2DynamoToken)
        self.engine.register(OAuth2DynamoClient)

        # Create the dynamo table for our registered model
        if create_tables:
            self.engine.create_schema()

    def save_token(self, token):
        print("saving token " + str(token.get_expires_in()))
        self.engine.save(token)

    def get_token(self, _access_token):
        token = self.engine.get(OAuth2DynamoToken, access_token=_access_token)
        if not token:
            raise InvalidTokenError()
        else:
            return token

    def delete_token(self, _user_id, _client_id):
        self.engine.delete_key(OAuth2DynamoToken, user_id=_user_id, client_id=_client_id)

    def get_client(self, _client_id):
        return self.engine.get(OAuth2DynamoClient, client_id=_client_id)

    def save_client(self, client):
        print("saving client id: " + str(client.client_id))
        self.engine.save(client)



# class OAuth2DynamoClient(Model):
#     """ Dynamo Implementation of Authlib's  OAuth 2 Client """
#     client_id = Field(type=STRING, hash_key=True)
#     client_secret = Field(type=STRING)
#     _client_metadata = Field(type=STRING)

#     def check_endpoint_auth_method(self, method, endpoint):
#         if endpoint == 'token':
#             # if client table has ``token_endpoint_auth_method``
#             return self.token_endpoint_auth_method == method
#         return True

#     @property
#     def client_info(self):
#         return dict(
#             client_id=self.client_id,
#             client_secret=self.client_secret
#         )

#     @cached_property
#     def client_metadata(self):
#         if self._client_metadata:
#             return json_loads(self._client_metadata)
#         return {}

#     def set_client_metadata(self, value):
#         self._client_metadata = json_dumps(value)

#     @property
#     def redirect_uris(self):
#         return self.client_metadata.get('redirect_uris', [])

#     @property
#     def token_endpoint_auth_method(self):
#         return self.client_metadata.get(
#             'token_endpoint_auth_method',
#             'client_secret_basic'
#         )

#     @property
#     def grant_types(self):
#         return self.client_metadata.get('grant_types', [])

#     @property
#     def response_types(self):
#         return self.client_metadata.get('response_types', [])

#     @property
#     def client_name(self):
#         return self.client_metadata.get('client_name')

#     @property
#     def client_uri(self):
#         return self.client_metadata.get('client_uri')

#     @property
#     def logo_uri(self):
#         return self.client_metadata.get('logo_uri')

#     @property
#     def scope(self):
#         return self.client_metadata.get('scope', '')

#     @property
#     def contacts(self):
#         return self.client_metadata.get('contacts', [])

#     @property
#     def tos_uri(self):
#         return self.client_metadata.get('tos_uri')

#     @property
#     def policy_uri(self):
#         return self.client_metadata.get('policy_uri')

#     @property
#     def jwks_uri(self):
#         return self.client_metadata.get('jwks_uri')

#     @property
#     def jwks(self):
#         return self.client_metadata.get('jwks', [])

#     @property
#     def software_id(self):
#         return self.client_metadata.get('software_id')

#     @property
#     def software_version(self):
#         return self.client_metadata.get('software_version')

#     def get_client_id(self):
#         return self.client_id

#     def get_default_redirect_uri(self):
#         if self.redirect_uris:
#             return self.redirect_uris[0]

#     def get_allowed_scope(self, scope):
#         if not scope:
#             return ''
#         allowed = set(self.scope.split())
#         scopes = scope_to_list(scope)
#         return list_to_scope([s for s in scopes if s in allowed])

#     def check_redirect_uri(self, redirect_uri):
#         return redirect_uri in self.redirect_uris

#     def has_client_secret(self):
#         return bool(self.client_secret)

#     def check_client_secret(self, client_secret):
#         return self.client_secret == client_secret

#     def check_token_endpoint_auth_method(self, method):
#         return self.token_endpoint_auth_method == method

#     def check_response_type(self, response_type):
#         return response_type in self.response_types

#     def check_grant_type(self, grant_type):
#         return grant_type in self.grant_types
# 