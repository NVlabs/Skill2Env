#!/usr/bin/env python3
"""CDK Custom Resource Lambda for AgentCore Gateway lifecycle management.

Handles create/update/delete of AgentCore Gateway resources via CloudFormation
Custom Resource events. Used in CDK stacks that deploy Gateway + Lambda targets.

This Lambda is invoked by CloudFormation during stack create/update/delete and
manages the AgentCore Gateway resource lifecycle through the boto3 API.

Environment Variables:
    GATEWAY_NAME: Name of the Gateway to manage
    TARGET_LAMBDA_ARN: ARN of the Lambda function to register as target
    OPENAPI_SCHEMA_S3_URI: S3 URI of the OpenAPI schema file
    GATEWAY_IAM_ROLE_ARN: IAM role ARN for Gateway to invoke Lambda
"""

import logging
import os
import time

import boto3
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client("bedrock-agentcore-control")


def handler(event, context):
    """CloudFormation Custom Resource handler."""
    request_type = event["RequestType"]
    try:
        if request_type == "Create":
            result = handle_create()
        elif request_type == "Update":
            result = handle_update(event)
        elif request_type == "Delete":
            result = handle_delete(event)
        else:
            raise ValueError(f"Unknown RequestType: {request_type}")

        physical_id = result.get("GatewayId", event.get("PhysicalResourceId", ""))
        cfnresponse.send(event, context, cfnresponse.SUCCESS, result, physical_id)
    except Exception:
        logger.exception(f"Custom resource {request_type} failed")
        physical_id = event.get("PhysicalResourceId", f"failed-{context.aws_request_id}")
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, physical_id)


def handle_create():
    """Create Gateway and register Lambda target."""
    gateway_name = os.environ["GATEWAY_NAME"]
    target_lambda_arn = os.environ["TARGET_LAMBDA_ARN"]
    schema_s3_uri = os.environ["OPENAPI_SCHEMA_S3_URI"]
    gateway_role_arn = os.environ["GATEWAY_IAM_ROLE_ARN"]

    response = client.create_gateway(
        name=gateway_name,
        protocolType="MCP",
        description=f"Gateway for {gateway_name}",
    )
    gateway_id = response["gatewayId"]
    logger.info(f"Created Gateway: {gateway_id}")

    try:
        wait_for_gateway_available(gateway_id)

        target_response = client.create_gateway_target(
            gatewayIdentifier=gateway_id,
            name=f"{gateway_name}-target",
            targetConfiguration={
                "lambdaTargetConfiguration": {
                    "lambdaArn": target_lambda_arn,
                    "roleArn": gateway_role_arn,
                }
            },
            schemaConfiguration={
                "s3": {"uri": schema_s3_uri},
            },
            description="Lambda target",
        )
    except Exception:
        logger.exception(f"Failed after creating Gateway {gateway_id}, cleaning up")
        _delete_gateway(gateway_id)
        raise

    return {
        "GatewayId": gateway_id,
        "TargetId": target_response.get("targetId", ""),
    }


def handle_update(event):
    """Update by replacing: create new gateway, then delete old one."""
    old_gateway_id = event.get("PhysicalResourceId", "")
    result = handle_create()
    if old_gateway_id:
        try:
            _delete_gateway(old_gateway_id)
        except Exception:
            logger.exception(
                f"Failed to delete old Gateway {old_gateway_id} during update. "
                f"New Gateway {result.get('GatewayId')} created successfully. "
                f"Manual cleanup of old Gateway may be required."
            )
    return result


def handle_delete(event):
    """Delete Gateway and all its targets."""
    gateway_id = event.get("PhysicalResourceId", "")
    if not gateway_id or gateway_id.startswith("failed-"):
        return {"Status": "Nothing to delete"}
    _delete_gateway(gateway_id)
    return {"Status": "Deleted"}


def _delete_gateway(gateway_id):
    """Delete a gateway and all its targets, ignoring not-found errors."""
    try:
        targets = client.list_gateway_targets(gatewayIdentifier=gateway_id)
        for target in targets.get("gatewayTargets", []):
            try:
                client.delete_gateway_target(
                    gatewayIdentifier=gateway_id,
                    targetIdentifier=target["targetId"],
                )
            except client.exceptions.ResourceNotFoundException:
                pass
        client.delete_gateway(gatewayIdentifier=gateway_id)
        logger.info(f"Deleted Gateway: {gateway_id}")
    except client.exceptions.ResourceNotFoundException:
        logger.info(f"Gateway {gateway_id} already deleted")


def wait_for_gateway_available(gateway_id, timeout=300, interval=10):
    """Poll until Gateway reaches AVAILABLE status."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            response = client.get_gateway(gatewayIdentifier=gateway_id)
        except Exception:
            logger.warning(f"Transient error polling Gateway {gateway_id}", exc_info=True)
            time.sleep(interval)
            continue
        status = response.get("status", "")
        if status == "AVAILABLE":
            return
        if status in ("FAILED", "DELETED"):
            reasons = response.get("failureReasons", [])
            raise RuntimeError(
                f"Gateway {gateway_id} reached terminal status: {status}. Reasons: {reasons}"
            )
        logger.info(f"Gateway {gateway_id} status: {status}, waiting...")
        time.sleep(interval)
    raise TimeoutError(f"Gateway {gateway_id} not available after {timeout}s")
