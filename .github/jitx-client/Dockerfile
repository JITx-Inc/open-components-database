FROM 657302324634.dkr.ecr.us-west-2.amazonaws.com/jitx-client:1.1.13-rc.31
# To pull this image locally, you need to authenticate with JITX's ECR assuming you have a jitx profile with credentials:
# aws ecr --profile jitx get-login-password --region us-west-2 | docker login --username AWS --password-stdin 657302324634.dkr.ecr.us-west-2.amazonaws.com

RUN apt update
RUN apt install -y python3.8

WORKDIR /app
COPY ./user.params /root/.jitx/user.params
COPY ./scripts/ scripts/
COPY ./license /root/.jitx/license

CMD ["/bin/bash", "scripts/run-ocdb-tests.sh"]
