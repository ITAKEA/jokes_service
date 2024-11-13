# hvis du har en mac m2 eller m3 skal du bruge denne from statement istedet for den jeg bruger
##############################################
# FROM --platform=Linux/amd64 python:3.9-slim
##############################################

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]