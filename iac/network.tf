resource "aws_vpc" "serasa_service" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = merge(local.tags, { "Name" : local.vpc_name })
}


resource "aws_network_acl" "acl" {
  vpc_id = aws_vpc.serasa_service.id

  ingress {
    protocol   = "tcp"
    rule_no    = 100
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = 3306
    to_port    = 3306
  }


  tags = merge(local.tags, { "Name" : local.acl_name })
}

resource "aws_subnet" "public_subnets" {
  count      = length(var.public_subnet_cidrs)
  vpc_id     = aws_vpc.serasa_service.id
  cidr_block = element(var.public_subnet_cidrs, count.index)

  availability_zone = element(var.azs, count.index)

  tags = merge(local.tags, { "Name" : "${local.public_subnet_name} ${count.index + 1}" })
}

#resource "aws_network_acl_association" "main" {
#  count          = length(var.public_subnet_cidrs)
#  subnet_id      = element(aws_subnet.public_subnets[*].id, count.index)
#  network_acl_id = aws_network_acl.acl.id
#}

resource "aws_subnet" "private_subnets" {
  count      = length(var.private_subnet_cidrs)
  vpc_id     = aws_vpc.serasa_service.id
  cidr_block = element(var.private_subnet_cidrs, count.index)

  availability_zone = element(var.azs, count.index)

  tags = merge(local.tags, { "Name" : "${local.private_subnet_name} ${count.index + 1}" })
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.serasa_service.id

  tags = merge(local.tags, { "Name" : local.internt_gateway_name })
}

resource "aws_route_table" "second_rt" {
  vpc_id = aws_vpc.serasa_service.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = merge(local.tags, { "Name" : local.route_table_name })
}

resource "aws_route_table_association" "public_subnet_asso" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = element(aws_subnet.public_subnets[*].id, count.index)
  route_table_id = aws_route_table.second_rt.id
}


resource "aws_security_group" "rds" {
  name = local.db_subnet_security_group_name

  vpc_id = aws_vpc.serasa_service.id

  ingress {
    from_port   = 0
    to_port     = 5432
    protocol    = "tcp"
    description = "Postgress"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { "Name" : local.db_subnet_security_group_name })
}
