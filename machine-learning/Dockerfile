FROM python:3.10

RUN pip install --upgrade pip \
    && pip install pandas scikit-learn

WORKDIR /app

COPY . .

WORKDIR /app/src
CMD ["python", "script.py"]

