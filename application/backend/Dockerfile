# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app/
COPY data /app/data/
copy imagenet_classes.json /app/

# Install any needed packages specified in requirements.txt
# Uncomment the line below if you have a requirements.txt file
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container (if your app uses it)
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]