import time
from authlib.oauth2.rfc6750 import InvalidTokenError
from flywheel import Engine
from .models import OAuth2DynamoToken, OAuth2DynamoClient

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
            self.create_client()

    def save_token(self, token):
        print("saving token " + str(token.get_expires_in()))
        self.engine.save(token)

    def get_token(self, _access_token):
        token = self.engine.get(OAuth2DynamoToken, access_token=_access_token)
        if not token:
            raise InvalidTokenError()
        else:
            return token
    
    def get_token_by_refresh(self, _refresh_token):
        token = self.engine.query(OAuth2DynamoToken).filter(OAuth2DynamoToken.refresh_token == _refresh_token).one()
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
 
    def create_client(self, c_id="CLIENT_ID", c_secret="secret"):
        client_id = c_id
        client_id_issued_at = int(time.time())
        client = OAuth2DynamoClient(
            client_id=client_id,
            client_id_issued_at=client_id_issued_at
        )

        client_metadata = {
            "client_name": "Client Name",
            "client_uri": "https://authlib.org/",
            "grant_types": ["password", "refresh_token"],
            "redirect_uris": ["https://authlib.org/"],
            "response_types": ["response_type", "code"],
            "scope": "profile",
            "token_endpoint_auth_method": "client_secret_basic"
        }
        client.set_client_metadata(client_metadata)
        client.client_secret = c_secret

        self.save_client(client)
