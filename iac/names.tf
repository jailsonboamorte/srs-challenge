locals {
  acl_name                      = "${var.PROJECT_NAME}-acl"
  api_gateway_name              = "${var.PROJECT_NAME}-api_gateway"
  db_instance_name              = "${var.PROJECT_NAME}-db"
  db_subnet_group_name          = "${var.PROJECT_NAME}-db_subnet_group"
  db_subnet_security_group_name = "${var.PROJECT_NAME}-db_subnet_security_group"
  ecr_repository_name           = "${var.PROJECT_NAME}-lambda"
  internt_gateway_name          = "${var.PROJECT_NAME}-internet_gateway"
  lambda_ecr_image_name         = "${var.PROJECT_NAME}-lambda"
  lambda_policy_name            = "${var.PROJECT_NAME}-lambda-policy"
  lambda_role_name              = "${var.PROJECT_NAME}-lambda-role"
  private_subnet_name           = "${var.PROJECT_NAME}-private_subnet"
  public_subnet_name            = "${var.PROJECT_NAME}-public_subnet"
  route_table_name              = "${var.PROJECT_NAME}-route_table"
  vpc_name                      = "${var.PROJECT_NAME}-vpc"

}
