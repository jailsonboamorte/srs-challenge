resource "aws_db_subnet_group" "db_subnet_group" {
  name       = local.db_subnet_group_name
  subnet_ids = [for subnet in aws_subnet.public_subnets : subnet.id]

  tags = merge(local.tags, { "Name" : local.db_subnet_group_name })
}

resource "aws_db_instance" "serasa_service" {
  allocated_storage      = 10
  db_name                = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)["DATABASE"]
  engine                 = "postgres"
  engine_version         = "15.14"
  identifier             = lower(local.db_instance_name)
  instance_class         = "db.t3.micro"
  username               = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)["USER"]
  password               = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)["PASSWORD"]
  skip_final_snapshot    = true
  publicly_accessible    = true
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.id
  vpc_security_group_ids = [aws_security_group.rds.id]
  tags                   = merge(local.tags, { "Name" : local.db_instance_name })
}
