FROM 335772445280.dkr.ecr.us-west-1.amazonaws.com/jitx-client:dev
# To pull this image locally, need to authenticate with Mike's ECR assuming you have an AWS Mike profile with credentials:
# aws ecr --profile mike get-login-password --region us-west-1 | docker login --username AWS --password-stdin 335772445280.dkr.ecr.us-west-1.amazonaws.com

ENV PATH="${PATH}:/root/.jitx/current/"

WORKDIR /app
COPY ./scripts/ scripts/

CMD ["/bin/bash", "scripts/run-ocdb-tests.sh"]
