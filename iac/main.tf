
provider "aws" {
  region = var.AWS_REGION
}

resource "aws_ecr_repository" "build_ecr_repository" {
  name                 = local.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  tags = merge(local.tags, { "Name" : local.ecr_repository_name })
}


resource "null_resource" "build_push_dkr_img" {
  triggers = {
    detect_docker_source_changes = var.force_image_rebuild == true ? timestamp() : local.dkr_img_src_sha256
  }

  provisioner "local-exec" {
    command = local.dkr_build_cmd
  }
}


