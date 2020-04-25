FROM python:3

WORKDIR /app

COPY . .

# Install dependencies.
ADD requirements.txt /app
RUN cd /app && \
    pip install -r requirements.txt

# Add actual source code.
#ADD blockchain.py /app
#ADD app.py /app
#COPY app.py /app

#EXPOSE 5000

#CMD ["python", "./blockchain.py", "--port", "5000"]
CMD ["python", "./bc00.py"]
