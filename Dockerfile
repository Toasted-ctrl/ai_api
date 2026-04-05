# Use Python image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /code

# Copy dependency file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY ./src /code/app

# Setting src as pythonpath
ENV PYTHONPATH=/code/app

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]