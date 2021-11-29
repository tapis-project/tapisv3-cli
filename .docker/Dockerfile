FROM python:3.9.9

RUN git clone https://github.com/tapis-project/tapisv3-cli/
RUN echo 'alias tapis="/tapisv3-cli/src/tapis.sh"' >> ~/.bashrc
WORKDIR /tapisv3-cli
RUN pip install -r requirements.txt
WORKDIR /tapisv3-cli/src