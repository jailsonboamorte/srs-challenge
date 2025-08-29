resource "aws_api_gateway_rest_api" "apiGateway" {
  name        = local.api_gateway_name
  description = "This is my API for ${var.PROJECT_NAME} purposes"
}

resource "aws_api_gateway_resource" "proxyResource" {
  rest_api_id = aws_api_gateway_rest_api.apiGateway.id
  parent_id   = aws_api_gateway_rest_api.apiGateway.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "anyMethod" {
  rest_api_id   = aws_api_gateway_rest_api.apiGateway.id
  resource_id   = aws_api_gateway_resource.proxyResource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambdaIntegration" {
  rest_api_id             = aws_api_gateway_rest_api.apiGateway.id
  resource_id             = aws_api_gateway_resource.proxyResource.id
  http_method             = aws_api_gateway_method.anyMethod.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = aws_lambda_function.lambda_ecr_image.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambdaIntegration
  ]

  rest_api_id = aws_api_gateway_rest_api.apiGateway.id
  stage_name  = "dev"
}
