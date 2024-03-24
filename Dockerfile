FROM python:3.9

# Set the working directory in the container

WORKDIR /app

# Copy the content of the local src directory to the working directory

COPY . /app

# Install any dependencies

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt stopwords

# Make port 5000 available to the world outside this container

EXPOSE 5000

# Command to run on container start

CMD [ "python", "app.py" ]





