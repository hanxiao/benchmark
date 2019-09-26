ARG GNES_IMG_TAG
FROM gnes/gnes:${GNES_IMG_TAG}

ADD *.py ./

ENTRYPOINT ["python", "app.py", "--grpc_port", "5566"]