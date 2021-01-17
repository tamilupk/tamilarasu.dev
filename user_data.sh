#!/bin/bash

# Install dependencies
sudo apt update
sudo apt install -y nodejs
sudo apt install -y git

# Install Yarn
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
sudo apt update
sudo apt install -y yarn

# Deploy Application
git clone https://github.com/tamilupk/tamilarasu.dev.git
cd tamilarasu.dev/
sudo yarn install

# Start
yarn global add forever
forever start bin/www