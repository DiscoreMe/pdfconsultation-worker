FROM python:3.7

WORKDIR /home/pdfconsultation

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["main.py"]