# ========================================
# =               Warning!               =
# ========================================
# This is Github Action docker-based image.
# It is not intended for local development!
#
# You can find docs about how to setup your own Github Action here:
# https://dotenv-linter.readthedocs.io/en/latest/pages/integrations/github-actions.html
#
# It can still be used as a raw image for your own containers.
# See `action.yml` in case you want to learn more about Github Actions.
# See it live:
# https://github.com/wemake-services/dotenv-linter/actions
#
# This image is also available on Dockerhub:
# https://hub.docker.com/r/wemakeservices/dotenv-linter

FROM python:3.7-alpine

LABEL maintainer="sobolevn@wemake.services"
LABEL vendor="wemake.services"

ENV DOTENV_LINTER_VERSION='0.1.5'
ENV REVIEWDOG_VERSION='v0.9.14'

RUN apk add --no-cache bash git wget
RUN pip install "dotenv-linter==$DOTENV_LINTER_VERSION" \
  # Installing reviewdog to optionally comment on pull requests:
  && wget -O - -q 'https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh' \
  | sh -s -- -b /usr/local/bin/ "$REVIEWDOG_VERSION"

COPY ./scripts/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
