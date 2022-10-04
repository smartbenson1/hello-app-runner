FROM public.ecr.aws/amazonlinux/amazonlinux:2

EXPOSE 8080
WORKDIR /srv
COPY . /srv

RUN yum update -y \
    && amazon-linux-extras enable python3.8 \
    && yum install -y \
	       python38-devel \
           python38 \
    && python3.8 -m pip install pip --upgrade \
    && ln -s /usr/local/bin/pip3 /usr/bin/pip3 \
    && ln -s /usr/bin/pydoc3.8 /usr/local/bin/pydoc \
    && ln -s /usr/bin/python3.8 /usr/local/bin/python \
    && ln -s /usr/bin/python3.8-config /usr/local/bin/python-config \
    && yum -y clean all --enablerepo='*' \
    && rm -rf /var/cache/yum

RUN pip3 install -r requirements.txt

CMD ["python", "./server.py"]
