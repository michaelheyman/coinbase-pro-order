# Use the Python base image
FROM python:3.12

# Set a working directory
WORKDIR /func

# Copy all the files from the local directory into the container
COPY . .

# Install the Functions Framework
RUN pip install functions-framework

# Install any dependencies of the function
RUN pip install -r requirements.txt
