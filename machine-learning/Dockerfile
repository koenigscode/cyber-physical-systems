FROM python:3.10

RUN pip install --upgrade pip \
    && pip install pandas scikit-learn skl2onnx 

WORKDIR /app

RUN mkdir model_output

COPY . .

WORKDIR /app/src
CMD ["python", "script.py"]
