locals {

  //////////////////////////////////////////////////////////////////////////////////////////////
  /////////////  Substitute below values to match your AWS account, region & profile ///////////
  ///////////////////////////////////////////////////////////////////////////////////////////// 
  ecr_reg   = "${var.AWS_ACCOUNT}.dkr.ecr.${var.AWS_REGION}.amazonaws.com" # ECR docker registry URI
  ecr_repo  = local.ecr_repository_name                                    # ECR repo name
  image_tag = var.DEPLOY_IMG_TAG                                           # image tag

  root_path     = "../"
  app_path      = "${local.root_path}app"
  dkr_file_path = "${local.root_path}docker"

  excluded_directories = ["${local.app_path}.ruff_cache", "${local.app_path}.pytest_cache"]

  include_files = [for file in fileset(".", "${local.app_path}/**") : file
    if alltrue([for dir in local.excluded_directories : !(startswith(file, dir))])
  ]
  dkr_img_src_sha256 = sha256(join("", local.include_files))

  dkr_build_cmd = <<-EOT
        
        docker build -t ${local.ecr_reg}/${local.ecr_repository_name}:${local.image_tag} \
            --build-context root=${local.root_path} -f ${local.dkr_file_path}/Dockerfile .

        aws ecr get-login-password --region ${var.AWS_REGION} | \
          docker login --username AWS --password-stdin ${local.ecr_reg}


        docker push ${local.ecr_reg}/${local.ecr_repository_name}:${local.image_tag}
        
    EOT

}

