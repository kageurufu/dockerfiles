FROM debian

# RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing tini openscad xvfb-run
RUN apt-get update \
 && apt-get install -y \
      xvfb libgl1-mesa-dri openscad \
 && rm -rf /var/lib/apt/lists/*

ADD colorschemes/* /usr/share/openscad/color-schemes/render/
ADD xvfb-run.sh /init.sh

VOLUME [ "/data" ]
WORKDIR /data

ENTRYPOINT [ "/init.sh" ]