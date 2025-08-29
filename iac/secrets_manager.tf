data "aws_secretsmanager_secret" "serasa-service-database-api" {
  name = "serasa-service-database-api"
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = data.aws_secretsmanager_secret.serasa-service-database-api.id
}
