#!make
include .env
PATH_TF=./iac

export DOCKER_PATH=docker


up:
	docker compose up --build
down:
	docker compose down --volumes --remove-orphans

#CMD ["uvicorn", "main:api", "--host", "0.0.0.0", , "--reload"]
run:
	docker compose exec ${APP_CONTAINER_NAME}  uvicorn main:api --host=0.0.0.0 --port=8000 --reload

ps:
	docker compose ps
exec: 
	docker compose exec -it ${APP_CONTAINER_NAME} /bin/bash

linter: 
	docker compose exec ${APP_CONTAINER_NAME} black ./ --check
	docker compose exec ${APP_CONTAINER_NAME} ruff check ./

format: 
	docker compose exec ${APP_CONTAINER_NAME} black ./
	docker compose exec ${APP_CONTAINER_NAME} ruff check ./ --fix

test-dev: 
	docker compose exec ${APP_CONTAINER_NAME} python -m pytest -o log_cli=true

TEST_NAME?= test_
test: 					
	docker compose exec ${APP_CONTAINER_NAME} python -m pytest -k $(TEST_NAME) --disable-pytest-warnings

MIGRATION_DESCRIPTION?= ''
migration-create: 
	docker compose exec ${APP_CONTAINER_NAME} alembic revision --autogenerate -m "$(MIGRATION_DESCRIPTION)"

migration-up: 
	docker compose exec ${APP_CONTAINER_NAME} alembic upgrade head

migration-down: 
	docker compose exec ${APP_CONTAINER_NAME} alembic downgrade base

seeds: 
	docker compose exec ${APP_CONTAINER_NAME} python seeds/seeding.py 

basics: 
	docker compose exec ${APP_CONTAINER_NAME} python models/basics.py

define tfdir
	 -chdir="${PATH_TF}"
endef

define tf_backend	
	-backend-config="bucket=${TF_BUCKET}" -backend-config="key=${TF_BACKEND_KEY}" -backend-config="region=${AWS_REGION}"	
endef

# -var="force_image_rebuild=true"
define tf_vars
	-var="force_image_rebuild=false" -var="DEPLOY_IMG_TAG=$(TAG)" -var="AWS_ACCOUNT=${AWS_ACCOUNT}" -var="PROJECT_NAME=${PROJECT_NAME}" -var="AWS_REGION=${AWS_REGION}" -var="ENV=dev" 
endef

tf-init:
	@terraform ${tfdir} init -upgrade ${tf_backend}	

tf-plan:	
	@terraform ${tfdir} plan -out=tf_planned ${tf_vars}

tf-apply:		
	@terraform ${tfdir} apply --auto-approve tf_planned 

tf-destroy:
	@terraform ${tfdir} destroy ${tf_vars}