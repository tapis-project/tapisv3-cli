# TapisV3 CLI

TapisV3 CLI is a command line interface tool written in python that wraps the tapipy library to enable user to make fast and efficient calls to tapisv3 APIs.

## Installation
### Step 1: Clone the repo

`git clone https://github.com/tapis-project/tapisv3-cli.git`

### Step 3: Run the install script located in the project root directory

`cd tapisv3-cli`

**then run**

`./install`

### Step 4: Source your .bashrc/.zshrc

**Linux:**

`source ~/.bashrc`

**MAC:**

`source ~/.zshrc`

## Quick start
In this quick start guide, you will learn all of the commands you need to be an effective user of the TapisV3 CLI.

### Step 0: Install the CLI

Steps for installing the TapisV3 CLI can be found above.

### Step 1: Start a Tapis shell

The tapis shell is the fastest and most conventient way to run commands with the TapisV3 CLI. It runs the CLI as a single continuous process rather than starting a new process everytime the `tapis` script is called. When working inside of a Tapis shell, you do not need to type `tapis` before every command. Simply type the command, then enter. Or if you're already authenticated with a Tapis deployment, simply hit enter and you will be prompted to select the API for which you want to run operations

$ `tapis shell`

### Step 2: Authenticate with a Tapis deployment

Type `login` and hit 'Enter' once inside of a Tapis shell

    t>>> login

You will be prompted to enter a base URL(must include protocol/scheme), a Tapis username, and that user's corresponding password.

    t>>> login
    *Tapis baseurl: https://tacc.tapis.io
    *Username: <username>
    *Password 🔒: 
    Authenticating with Tapis at https://tacc.tapis.io for user <username>
    ✓ Successfully authenticated
    ✓ Created profile for user <username>

### Step 3: View available commands using the 'help' command

Type 'help' and press enter to view commands. You will see a list of core commands that are not specific to Tapis at the top. These commands can be used to customize your experience with the CLI as well as to switch between different user profiles and modify CLI display settings.

    t>>> help

    General utilities
    shell - Starts a tapis shell that enables users to run multiple commands directly to the cli API in a single process (cannot run nested shells)
    login - Authenticates with a Tapis deployment and creates user profile
    profile - List, remove, and switch to different user profiles
    packages - List and switch between packages
    set - Modify cli output type and output directory for file output types
    info - Show current user, packages, and auth info

    Info: Generating help info...

    Package Specific Commands for the 'tapis' package
    Interactive mode
    Run `$tapis` in a shell (or when in a tapis shell, just press the `enter/return` key) and you will be prompted to choose an api and operation to run

    Manual mode
    Usage $tapis [api] [operation_id]
    Example $tapis system getSystems --systemId my-system-id


    actors - run operations on the Tapis Actors API 
    authenticator - run operations on the Tapis Authenticator API 
    meta - run operations on the Tapis Meta API 
    files - run operations on the Tapis Files API 
    sk - run operations on the Tapis Sk API 
    streams - run operations on the Tapis Streams API 
    systems - run operations on the Tapis Systems API 
    tenants - run operations on the Tapis Tenants API 
    tokens - run operations on the Tapis Tokens API 
    pgrest - run operations on the Tapis Pgrest API 
    pods - run operations on the Tapis Pods API 
    jobs - run operations on the Tapis Jobs API 
    apps - run operations on the Tapis Apps API 
    workflows - run operations on the Tapis Workflows API 
    notifications - run operations on the Tapis Notifications API


### Step 4: Run the 'getSystems' operation on the Systems API

This step will produce a list of systems available to you for a given tenant formatted as a table. **Note** the default view for results is `table`. We will modify the display settings later to change the format of the table as well as change to output type so we can retrieve the JSON data returned from a Tapis call.

From the Tapis shell, simply hit enter to choose the API you want to run operations for:

    t>>> 

Select `systems` from the dropdow list:

    [?] Select an API: actors
    actors
    apps
    authenticator
    files
    jobs
    meta
    notifications
    pgrest
    pods
    sk
    streams
    > systems
    tenants

Then select the `getSystems` operation:

    [?] Select an operation: getSystems
    getGlobusAuthUrl
    getHistory
    getSchedulerProfile
    getSchedulerProfiles
    getShareInfo
    getSystem
    > getSystems
    getUserCredential
    getUserPerms
    grantUserPerms
    healthCheck
    isEnabled
    matchConstraints

You will then be prompted to input values for optional query params. Skip through all of them by pressing 'Enter' when prompted for each parameter:

    Query parameters:
    search: 
    listType: 
    limit: 
    orderBy: 
    skip: 
    startAfter: 
    computeTotal: 
    select: 
    showDeleted: 

Your result will then be displayed as a table in the shell:

    Warning: Only showing the first 8 columns
    ╒════╤════════════════════════╤══════════════╤══════════╤═══════════════╤═══════════════════╤══════════════════════╤═══════════╤════════════╕
    │    │ id                     │ systemType   │ owner    │ host          │ effectiveUserId   │ defaultAuthnMethod   │ canExec   │ parentId   │
    ╞════╪════════════════════════╪══════════════╪══════════╪═══════════════╪═══════════════════╪══════════════════════╪═══════════╪════════════╡
    │  0 │ test-1                 │ LINUX        │ nathandf │ 129.114.35.53 │ testuser2         │ PKI_KEYS             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  1 │ newsystem              │ LINUX        │ nathandf │ 129.114.35.53 │ testuser2         │ PKI_KEYS             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  2 │ presentation           │ LINUX        │ nathandf │ 129.114.35.53 │ testuser2         │ PKI_KEYS             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  3 │ tapisv3-exec-nathandf2 │ LINUX        │ nathandf │ 129.114.35.53 │ nathandf          │ PASSWORD             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  4 │ tapisv3-exec-nathandf3 │ LINUX        │ nathandf │ 129.114.35.53 │ nathandf          │ PASSWORD             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  5 │ tapisv3-exec-nathandf  │ LINUX        │ nathandf │ 129.114.35.53 │ nathandf          │ PASSWORD             │ true      │ null       │
    ├────┼────────────────────────┼──────────────┼──────────┼───────────────┼───────────────────┼──────────────────────┼───────────┼────────────┤
    │  6 │ testuser2.execution    │ LINUX        │ nathandf │ 129.114.35.53 │ testuser2         │ PKI_KEYS             │ true      │ null       │
    ╘════╧════════════════════════╧══════════════╧══════════╧═══════════════╧═══════════════════╧══════════════════════╧═══════════╧════════════╛













