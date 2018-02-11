#!/bin/bash

cd /tmp

# Redis Defaults
REDIS_URL="http://download.redis.io/releases/redis-stable.tar.gz"
REDIS_TGZ="redis-stable.tar.gz"
REDIS_DIR="redis-stable"

# Download and unpack Redis
wget $REDIS_URL
tar zxf $REDIS_TGZ

# Move into the directory and build
cd $REDIS_DIR
make && make install

cd utils/
echo -n | ./install_server.sh
