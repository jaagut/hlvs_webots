#! /bin/bash

# protoc --python_out=. ./robocup.proto
protoc --python_out=. --mypy_out=. ./robocup_extension.proto
