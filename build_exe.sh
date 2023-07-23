#!/usr/bin/env sh

pyinstaller \
    --clean \
    --onefile \
    --windowed \
    --name functino \
    --add-data "src/functino/resources:functino/resources" \
    src/functino/gui/__init__.py
