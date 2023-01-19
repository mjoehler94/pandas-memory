FROM amd64/python:3.9.16-slim-bullseye

WORKDIR /code

# install dependencies
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src ./src


# # start the server
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
# CMD ["python"]

# ENTRYPOINT ["/bin/bash"]
