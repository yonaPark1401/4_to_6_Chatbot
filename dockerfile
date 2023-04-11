FROM python:3.10
COPY . .
RUN pip install -r requirements.txt
ADD main.py .
CMD ["python", "./main.py"]
