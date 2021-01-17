#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y nodejs
sudo apt install -y npm
sudo apt install -y git
npm install -g yarn

# Deploy Application
git clone https://github.com/tamilupk/tamilarasu.dev.git
cd tamilarasu.dev/
yarn install

# Start
npm install forever -g
forever start bin/www