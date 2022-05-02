FROM ubuntu:22.04 AS base

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y \
        unzip \
        libgl1 \
        libx11-6 \
        libgtk-3-0 libgtk2.0-0 \
        libpangocairo-1.0-0 \
        libpango-1.0-0 \
        libgdk-pixbuf-2.0-0 \
        libglib2.0-0 \
        libdbus-1-3 \
        locales \
        ca-certificates \
        dbus-x11 \
        gosu \
        xdg-utils \
        xpra \
        menu-xdg \
        thunar xfce4-terminal \
 && echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen \
 && locale-gen \
 && rm -rf /var/lib/apt/lists/*

#  -------------------

FROM base
ARG UID=1000
ARG GID=1000
ARG SUPERSLICER=

COPY unpack-superslicer /tmp/unpack-superslicer
COPY superslicer-releases/${SUPERSLICER} /tmp/
RUN mkdir -p /config /run/dbus /run/user/0 /run/user/1000 /run/xpra /superslicer \
 && /tmp/unpack-superslicer ${SUPERSLICER} \
 && addgroup --gid $UID superslicer \
 && adduser --uid $UID --gid $GID --home /home/superslicer superslicer \
 && chown -R ${UID}:${GID} /config /superslicer /run/user/1000 /run/xpra

COPY entrypoint.sh /entrypoint.sh
COPY start_superslicer.sh /start_superslicer.sh

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV DBUS_SYSTEM_BUS_ADDRESS="unix:path=/var/run/dbus/system_bus_socket"
ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/var/run/dbus/session_bus_socket"
ENV XDG_RUNTIME_DIR=/tmp/

WORKDIR /home/superslicer

VOLUME [ "/config" ]
VOLUME [ "/home/superslicer/models" ]

EXPOSE 10000
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/usr/bin/xpra", "start", "--daemon=no", "--bind-tcp=0.0.0.0:10000", "--mdns=no", "--webcam=no", "--microphone=off", "--sharing=yes", "--printing=no", "--file-transfer=yes", "--min-quality=50", "--video-scaling=20",  "--start-on-connect=/start_superslicer.sh" ]
