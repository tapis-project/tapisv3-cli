# TapisV3 CLI

TapisV3 CLI is a command line interface tool written in python that wraps the tapipy library to enable user to make fast and efficient calls to tapisv3 APIs.

## Installation
tapis-cli can be set up and run in 2 ways; Locally, and in a Docker container.

### Local setup
**Step 1: Clone the repo**
`https://github.com/tapis-project/tapisv3-cli.git`

**Step 3: Run the install script located in the project root directory**
`./install`

**Step 4: Source your .bashrc/.zshrc**
`source ~/.bashrc`

### Container setup
NOTE: You must have docker installed locally for this to work
`cd` into the root directory of the project

## Build the image
`docker build -f .docker/Dockerfile -t tapisv3-cli:latest .`

## Run the container interactively
docker run -it tapisv3-cli:latest bash

## Configuring Tapis CLI
Tapis CLI must first be configured. Run the following command and add your credentials\
$`tapis configure`

