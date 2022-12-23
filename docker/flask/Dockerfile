FROM python:3.9-slim-bullseye

# Mount src directory to /app
ADD ./src /app
WORKDIR /app

# Use virtual environment
#ENV VIRTUAL_ENV=/app/
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose Port
EXPOSE 5000

# Install dependencies
RUN pip install -r requirements.txt
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
