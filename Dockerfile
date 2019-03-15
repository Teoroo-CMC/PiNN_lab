# this is our first build stage, it will not persist in the final image
FROM jupyter/tensorflow-notebook:latest as intermediate

# install git
USER root
RUN apt-get update
RUN apt-get install -y git ssh

# add credentials on build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN cd /
RUN git clone git@github.com:Teoroo-CMC/PiNN_dev.git
RUN git clone git@github.com:Teoroo-CMC/PiNN_lab.git 

FROM jupyter/tensorflow-notebook:latest
USER root
# copy the repository form the previous image
COPY --from=intermediate /PiNN_dev /srv/PiNN
COPY --from=intermediate /PiNN_dev /srv/PiNN_lab
RUN cd /srv/PiNN && pip install -e .
RUN pip install jupyter-tensorboard tensorflow-tensorboard tensorboard
RUN cp -r /srv/PiNN/doc/notebooks /opt/doc
RUN cp -r /srv/PiNN_lab/lab_session /opt/lab_session
RUN jupyter tensorboard enable --sys-prefix
