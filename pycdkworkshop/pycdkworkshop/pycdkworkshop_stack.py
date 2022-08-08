from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_apigateway as api,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
)


class PycdkworkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "PycdkworkshopQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "PycdkworkshopTopic"
        )

        bucket = s3.Bucket(
            self,
            id='s3cdkbucket',
            bucket_name='examplecdkbucket',
            versioned=True
        )

        lambdaFunction = _lambda.Function(
            self,
            id="lambdafunction",
            code= _lambda.Code.from_asset(
                path='lambdacode'
            ),
            handler= 'hello.handler',
            runtime= _lambda.Runtime.PYTHON_3_9
        )

        lambdaApi = api.LambdaRestApi(
            self,
            id='restapi',
            handler=lambdaFunction
        )

        topic.add_subscription(subs.SqsSubscription(queue))
