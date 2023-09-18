FROM python:3.9-alpine3.16

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install flask only
RUN pip install -r requirements.txt

# Run server.py when the container launches
CMD ["flask", "run"]