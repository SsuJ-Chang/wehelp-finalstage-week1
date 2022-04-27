FROM python:3.10.0

WORKDIR /final_stage_w1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "python3", "-m" , "app", "run", "--host=0.0.0.0"]