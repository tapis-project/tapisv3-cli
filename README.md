# TapisV3 CLI

TapisV3 CLI is a command line interface tool written in python that wraps the tapipy library to enable user to make fast and efficient calls to tapisv3 APIs.

### Local installation
**Step 1: Clone the repo**
`git clone https://github.com/tapis-project/tapisv3-cli.git`

**Step 3: Run the install script located in the project root directory**
`cd tapisv3-cli`

`./install`

**Step 4: Source your .bashrc/.zshrc**
`source ~/.bashrc`

### Docker install

**Step 1: Build the image**
`docker pull tapis/tapisv3-cli:latest`

**Step 2: Run the container interactively**
`docker run -it tapis/tapisv3-cli:latest bash`

**Step 3: Login to Tapis**
`tapis login`

