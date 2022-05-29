FROM python:3.6
ENV PYTHONUNBUFFERED=1

ADD ./requirement.txt /requirement.txt 
RUN pip3 install -r /requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
ADD ./web_server /web_server
WORKDIR /web_server

