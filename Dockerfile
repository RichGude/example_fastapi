# Setting up a Docker image, start with a base image
FROM python:3.9.7

# Specifiying the work directory allows all future directory calls to forgo listing the precedents
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all of the files after pip so as to avoid rerunning the pip install if any other file changes
COPY . .

# To run multiple commands in the Docker container (namely alembic and uvicorn), use a shell command
#   alembic upgrade head [to upgrade database with correct schema]
#   uvicorn app.main:app --host 0.0.0.0 --port 8000
ADD start.sh /
RUN chmod +x /start.sh

CMD ["/start_dev.sh"]

# Break up every word in the starting command into elements in a Docker list

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]