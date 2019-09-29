FROM amancevice/pandas:0.25.0

RUN pip install matplotlib

ADD *.py ./

ENTRYPOINT ["python", "app.py"]