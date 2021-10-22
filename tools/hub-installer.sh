#!/usr/bin/env bash
set -e

wget https://github.com/github/hub/releases/download/v2.12.3/hub-linux-amd64-2.12.3.tgz -q
tar -xzf hub-linux-amd64-2.12.3.tgz
mv hub-linux-amd64-2.12.3 /opt/tools/hub
