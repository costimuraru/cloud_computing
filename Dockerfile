FROM python:3.9

RUN mkdir /blog
WORKDIR /blog
ADD . /blog
RUN pip install -r requirements.txt
EXPOSE 8000
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
