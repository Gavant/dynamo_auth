# Dynamo_Auth

A small oauth package using [authlib](https://docs.authlib.org/en/latest/) and [flywheel](https://flywheel.readthedocs.io/en/latest/). Replaces some authlib sqlalchemy mixins with dynamodb classes

## Setup

- to connect the Dynamo object to an existing db run init_engine with the args **dy_region, use_local** set
    ```
    init_engine('us-east-1', False)
    ```

- to create the dynamo tables and client item run init_engine with create_tables=True and client_id, client_secret, and client_metadata also set
     ```
     my_client_metadata = {
                "client_name": "Client Name",
                "grant_types": ["password", "refresh_token"],
                "scope": "profile", "admin",
                "token_endpoint_auth_method": "client_secret_basic"
            }
    
    init_engine('us-east-1', False, create_tables=True, client_id='some_id', client_secret='some_secre', client_metadata=client_metadata)
    ```


## Models

1. ### DynamoPasswordResetToken
    - verifies a user's password reset request
    - no indices
  
2. ### OAuth2DynamoToken
    - oauth2 access token
    - dynamo version of authlib.integrations.sqla_oauth2.OAuth2TokenMixin
    - global index on refresh_token and user_id. Both only project hash key

3. ### OAuth2DynamoClient
   - dynamo version of authlib.integrations.sqla_oauth2.OAuth2ClientMixin
   - has client id, secret, and metadata
   - no indices