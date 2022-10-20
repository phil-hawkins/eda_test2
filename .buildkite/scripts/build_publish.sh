#!/usr/bin/env bash

set -euo pipefail

docker build --no-cache --rm -t "${RQP_APPLICATION}" .
