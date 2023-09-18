FROM python:3.9-alpine3.16

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install all lib need in requirements.txt
RUN pip install -r requirements.txt

# Run the client script when the container launches
CMD ["python", "client.py"]