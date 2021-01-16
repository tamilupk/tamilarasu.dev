#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y nodejs
sudo apt install -y npm
sudo apt install -y git

# Deploy Application
git clone https://github.com/tamilupk/tamilarasu.dev.git
cd tamilarasu.dev/
npm install

# Start
npm install forever -g
forever start bin/www