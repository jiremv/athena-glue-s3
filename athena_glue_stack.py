from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_glue as glue,
    aws_stepfunctions as sfn,
    RemovalPolicy,
    Aws
)
from constructs import Construct
import json

class AthenaGlueS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        athena_bucket = s3.Bucket(self, "AthenaQueryS3Bucket",
                                  removal_policy=RemovalPolicy.DESTROY,
                                  auto_delete_objects=True)

        crawler_bucket = s3.Bucket(self, "CrawlerS3Bucket",
                                   removal_policy=RemovalPolicy.DESTROY,
                                   auto_delete_objects=True)

        my_database = glue.CfnDatabase(self, "MyDatabase",
                                       catalog_id=Aws.ACCOUNT_ID,
                                       database_input={"name": "my_database"})

        my_role = iam.Role(self, "MyRole",
                           assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
                           managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")])

        my_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:PutObject"],
            resources=[f"{crawler_bucket.bucket_arn}/*"]
        ))

        glue.CfnCrawler(self, "MyCrawler",
                        name="testcrawler",
                        role=my_role.role_arn,
                        database_name=my_database.ref,
                        targets={"s3Targets": [{"path": f"{crawler_bucket.bucket_arn}/"}]})

        sf_role = iam.Role(self, "SFRole",
                           assumed_by=iam.ServicePrincipal("states.amazonaws.com"))

        sf_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "athena:startQueryExecution",
                "athena:stopQueryExecution",
                "athena:getQueryExecution",
                "athena:getDataCatalog",
                "athena:getQueryResults"
            ],
            resources=["*"]
        ))

        sf_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "s3:GetBucketLocation",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload",
                "s3:CreateBucket",
                "s3:PutObject"
            ],
            resources=[
                athena_bucket.bucket_arn,
                f"{athena_bucket.bucket_arn}/*",
                crawler_bucket.bucket_arn,
                f"{crawler_bucket.bucket_arn}/*"
            ]
        ))

        sf_role.add_to_policy(iam.PolicyStatement(
            actions=[
                "glue:CreateDatabase",
                "glue:GetDatabase",
                "glue:GetDatabases",
                "glue:UpdateDatabase",
                "glue:DeleteDatabase",
                "glue:CreateTable",
                "glue:UpdateTable",
                "glue:GetTable",
                "glue:GetTables",
                "glue:DeleteTable",
                "glue:BatchDeleteTable",
                "glue:BatchCreatePartition",
                "glue:CreatePartition",
                "glue:UpdatePartition",
                "glue:GetPartition",
                "glue:GetPartitions",
                "glue:BatchGetPartition",
                "glue:DeletePartition",
                "glue:BatchDeletePartition"
            ],
            resources=["*"]
        ))

        with open("athenaquery.asl.json", "r") as definition_file:
            definition_string = json.dumps(json.load(definition_file))

        sfn.CfnStateMachine(self, "StateMachine",
                            role_arn=sf_role.role_arn,
                            definition_string=definition_string,
                            state_machine_name="StateMachine")
