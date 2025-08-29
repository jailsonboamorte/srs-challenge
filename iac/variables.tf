variable "AWS_ACCESS_KEY_ID" {
  type    = string
  default = null
}

variable "AWS_SECRET_ACCESS_KEY" {
  type    = string
  default = null
}

variable "AWS_SESSION_TOKEN" {
  type      = string
  default   = null
  sensitive = true
}

variable "MYSQL_DATABASE" {
  type      = string
  default   = null
  sensitive = true
}

variable "MYSQL_USER" {
  type      = string
  default   = null
  sensitive = true
}
variable "MYSQL_PASSWORD" {
  type      = string
  default   = null
  sensitive = true
}


variable "AWS_REGION" {
  type    = string
  default = null
}

variable "AWS_ACCOUNT" {
  type    = string
  default = null
}

variable "PROJECT_NAME" {
  type    = string
  default = null
}
variable "DEPLOY_IMG_TAG" {
  type    = string
  default = null
}

variable "force_image_rebuild" {
  type    = bool
  default = true
}
variable "timezone" {
  type    = string
  default = "America/Sao_Paulo"
}

variable "ENV" {
  type    = string
  default = "local"
}

variable "public_subnet_cidrs" {
  type        = list(string)
  description = "Public Subnet CIDR values"
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  type        = list(string)
  description = "Private Subnet CIDR values"
  default     = ["10.0.4.0/24"]
}

variable "azs" {
  type        = list(string)
  description = "Availability Zones"
  default     = ["us-east-1a", "us-east-1b"]
}
