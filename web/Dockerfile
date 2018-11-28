FROM python:3.6-alpine
ADD . /workdir
WORKDIR /workdir
RUN pip install -r requirements.txt
CMD ["python", "main.py"]