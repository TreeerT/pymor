ARG BASE=pymor/jupyter_py3.8:latest
FROM ${BASE}
MAINTAINER rene.fritze@wwu.de

ENV PYTHONPATH=/pymor/src:${PYTHONPATH}
ARG NB_USER=pymor
ARG NB_UID=1000
ARG PYMOR_JUPYTER_TOKEN=pyMOR_token

USER root
RUN useradd -d /home/pymor --shell /bin/bash -u ${NB_UID} -o -c "" -m ${NB_USER} && \
    chown -R ${NB_USER} /home/pymor

# do local package install before requirements to avoid conflict
COPY .binder/local_packages /pymor/local_packages/
RUN (for i in $(find /pymor/local_packages -maxdepth 1 -mindepth 1 -type d | grep -v keepdir) ; do pip install -e $i ; done) \
  && rm -rf /pymor/local_packages
USER ${NB_USER}

ENV JUPYTER_TOKEN=${PYMOR_JUPYTER_TOKEN} \
    USER=${NB_USER} \
    HOME=/home/pymor

ENTRYPOINT []
WORKDIR /pymor/
