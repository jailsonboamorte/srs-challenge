# LAMBDA ECR IMAGE
resource "aws_lambda_function" "lambda_ecr_image" {
  function_name = local.lambda_ecr_image_name
  description   = "Serasa Service"

  role = aws_iam_role.lambda_role.arn

  memory_size = 512
  timeout     = 600
  ephemeral_storage {
    size = 512
  }
  reserved_concurrent_executions = 5



  image_uri    = "${var.AWS_ACCOUNT}.dkr.ecr.${var.AWS_REGION}.amazonaws.com/${local.ecr_repository_name}:${var.DEPLOY_IMG_TAG}"
  package_type = "Image"
  environment {
    variables = {
      ENV                        = var.ENV
      PROJECT_NAME               = var.PROJECT_NAME
      SM_SERASA_SERVICE_DATABASE = "serasa-service-database-api"
    }
  }

  depends_on = [null_resource.build_push_dkr_img]
  tags       = merge(local.tags, { "Name" : local.lambda_ecr_image_name })
}

resource "aws_lambda_alias" "lambda_ecr_image_alias" {
  name             = "${var.PROJECT_NAME}-lambda-alias"
  function_name    = aws_lambda_function.lambda_ecr_image.function_name
  function_version = aws_lambda_function.lambda_ecr_image.version
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_ecr_image.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.apiGateway.execution_arn}/*/*/{proxy+}"
}
