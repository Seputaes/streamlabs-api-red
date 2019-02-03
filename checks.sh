#!/usr/bin/env bash

if grep -RnwIq --exclude-dir={\.tox,htmlcov} --exclude={Makefile,\*.sh,\*.ini} . -e "cog_shared"; then
  echo "ERROR: cog_shared found in seplib"
  exit 1
else
  exit 0
fi
