FROM python:3.11-alpine3.20

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Copy source code
COPY ./api /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# workers = (2 x no_of_cores) + 1
# Run API!
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "main:create_app()"]
