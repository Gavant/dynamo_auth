import time

def dynamo_create_save_token_func(dynamo, token_model):
    """ dynamo save_token function for authlib.integrations.flask_oauth2.AuthorizationServer's save_token param """
    def save_token(token, request):
        if request.user:
            user_id = request.user.get_user_id()
        else:
            user_id = None
        client = request.client
        item = token_model(
            client_id= client.client_id,
            user_id= user_id,
            issued_at= int(time.time()),
            token_type= token["token_type"],
            access_token= token["access_token"],
            expires_in= token["expires_in"],
            refresh_token= token["refresh_token"],
            scope= token["scope"] if "scope" in token else ""
        )
        dynamo.save_token(item)
    return save_token


def dynamo_create_query_client_func(dynamo):
    """ dynamo query_client for authlib.integrations.flask_oauth2.AuthorizationServer's query_client """

    def query_client(client_id):
        return dynamo.get_client(client_id)
    return query_client

def dynamo_create_bearer_token_validator(dynamo):
    """Token validator. dynamo version of authlib.oauth2.rfc6750.BearerTokenValidator"""
    from authlib.oauth2.rfc6750 import BearerTokenValidator
    class _BearerTokenValidator(BearerTokenValidator):
        def authenticate_token(self, token_string):
            return dynamo.get_token(token_string)

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            return token.revoked

    return _BearerTokenValidator

def dynamo_create_revocation_endpoint(dynamo):
    """ dynamo version of revocation endpoint class from uthlib.oauth2.rfc7009.RevocationEndpoint"""
    from authlib.oauth2.rfc7009 import RevocationEndpoint

    class _RevocationEndpoint(RevocationEndpoint):
        def query_token(self, token_string, token_type_hint, client):
            return dynamo.get_token(token_string)

        def revoke_token(self, token):
            token.revoked = True
            dynamo.save_token(token)

    return _RevocationEndpoint

