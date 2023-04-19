FROM public.ecr.aws/lambda/python:3.10

COPY src/. ${LAMBDA_TASK_ROOT}/src/
COPY Pipfile ${LAMBDA_TASK_ROOT}

RUN python3.10 -m pip install pipenv
RUN python3.10 -m pipenv install
RUN python3.10 -m pipenv requirements > ${LAMBDA_TASK_ROOT}/requirements.txt
RUN python3.10 -m pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

RUN python3.10 -m pipenv --rm
RUN rm ${LAMBDA_TASK_ROOT}/requirements.txt
RUN rm ${LAMBDA_TASK_ROOT}/Pipfile
RUN rm ${LAMBDA_TASK_ROOT}/Pipfile.lock
RUN python3.10 -m pip uninstall -y pipenv

CMD ["src.handler.lambda_handler"]