FROM python:3.8.13-alpine
WORKDIR /navis-work-dir
ADD . /navis-work-dir
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","app.py"]

# docker build --tag navis:1.0 .
# docker run  -p 5000:8080 navis:1.0
