From python:3.8.16
MAINTAINER Minyang
COPY . /qa_system
WORKDIR /qa_system
RUN mkdir -p /qa_system/volume /
RUN apt update /
RUN apt install -y default-jdk /
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
EXPOSE 8000
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["echo 1"]