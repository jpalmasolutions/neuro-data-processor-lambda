FROM public.ecr.aws/lambda/python:3.9

COPY src/. ${LAMBDA_TASK_ROOT}/src/
COPY requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt

CMD ["src.handler.lambda_handler"]