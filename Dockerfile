FROM python:3

WORKDIR /app

COPY . .

# Install dependencies.
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

CMD ["python", "./bc.py"]
