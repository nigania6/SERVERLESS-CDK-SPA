#!/usr/bin/env python3
import os
import aws_cdk as cdk
from serverless_spa_cdk.serverless_spa_cdk_stack import ServerlessSpaCdkStack

app = cdk.App()
ServerlessSpaCdkStack(app, "ServerlessSpaCdkStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

app.synth()

