# Use the official lightweight Python image.
FROM python:3.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Expose the port Gunicorn will run on
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Run the web service on container startup. Here we use the Gunicorn webserver,
# with one worker process and 8 threads. For environments with multiple CPU cores,
# increase the number of workers to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "src.app:app"]