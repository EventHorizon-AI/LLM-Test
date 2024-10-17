FROM ubuntu:latest
WORKDIR /app
RUN apt-get update && apt-get install -y curl python3.11 python3-pip
RUN pip3 install --upgrade pip
ADD ["./*.py", "requirements.txt"] /app
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py /app/data/input.json", "--output /app/data/output.json", "--base_url $OPENAI_BASEUFL", "--api_key $OPENAI_API_KEY", "--model $OPENAI_MODEL_NAME", "--num $TEST_NUM"]