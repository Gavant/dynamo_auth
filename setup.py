from setuptools import setup

setup(
    name='dynamo_auth',
    version='0.0.1',
    url='https://github.com/mgoldman-gavant/dynamo_auth',
    install_requires=[
        "sqlalchemy-aurora-data-api==0.2.7",
        "aurora-data-api==0.2.7",
        "bcrypt",
        "flywheel",
        "Authlib==0.14.3"
    ],
)
