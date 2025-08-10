# 1. Use Python 3.10 base image
FROM python:3.10

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set work directory inside container
WORKDIR /app

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy project files into container
COPY . /app/

# 6. Expose Django's default port
EXPOSE 8000

# 7. Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
