#!/bin/sh

if [ $# -eq 0 ]; then
  xvfb-run /bin/bash
else
  xvfb-run "$@"
fi