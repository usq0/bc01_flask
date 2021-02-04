FROM python:3.6

MAINTAINER https://github.com/usq0/bc01_flask

EXPOSE 5000

WORKDIR /app

COPY . .

# Install dependencies.
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

CMD ["python", "./bc.py"]
