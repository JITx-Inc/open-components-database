FROM 657302324634.dkr.ecr.us-west-2.amazonaws.com/jitx-client:2.24.0
# To pull this image locally, you need to authenticate with JITX's ECR assuming you have a jitx profile with credentials:
# aws ecr --profile jitx get-login-password --region us-west-2 | docker login --username AWS --password-stdin 657302324634.dkr.ecr.us-west-2.amazonaws.com

RUN apt update
RUN apt install -y python3.10

WORKDIR /app
COPY ./user.params /root/.jitx/user.params
COPY ./license /root/.jitx/license

CMD ["/bin/bash", "-c", "cd open-components-database ; scripts/run-ocdb-tests.sh"]
