locals {
  tags = {
    "Environment" = "${var.ENV}"
    "Service"     = "${var.PROJECT_NAME}"
  }
}
