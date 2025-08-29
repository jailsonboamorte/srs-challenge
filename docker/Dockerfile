FROM public.ecr.aws/lambda/python:3.12

# CODE
COPY --from=root ./pyproject.toml .

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

#dnf install -y postgresql-devel && \
#dnf install -y curl && \
# PYTHON ENV
RUN dnf -y update && \
    dnf install -y gcc postgresql-devel && \
    dnf clean all

    RUN pip install --upgrade pip==24.2 --no-cache-dir
RUN pip3 install poetry==1.8.3 --no-cache-dir
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY --from=root ./app ${LAMBDA_TASK_ROOT}

CMD ["main.handler"]