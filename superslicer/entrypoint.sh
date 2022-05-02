#!/bin/bash

dbus-daemon --system --fork --address=unix:path=/var/run/dbus/system_bus_socket
dbus-daemon --session --fork --address=unix:path=/var/run/dbus/session_bus_socket

set -xeuo pipefail
exec gosu superslicer:superslicer "$@"
