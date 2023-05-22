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

### Step 5 (Optional): Change the display settings to show more columns in a table

Notice that there is a warning at the top of the table.

    Warning: Only showing the first 8 columns

To ensure that tables are displayed correctly in the shell, only 8 columns will be shown by default. You can change these settings by running the `set` command and choosing `display_settings`. You will then be prompted to input values for all avalable display properties. To keep defaults, just press enter for each prompt.

    t>>> set
    [?] Perform action: display_settings
    > display_settings
    jwt
    output_dir
    output_type
    username

    *Maximum # of columns to display in table view (int) [8]: 
    *Maximum # of characters per column (int) [16]: 
    *List of properties exempt from trunction (comma-seperated list of strings) [id,uuid]: 
    *Column name to show first tables: Ex: 'id', 'uuid', 'jobUuid' [id]: 
    ✓ Display settings updated

### Step 6: Change the output type so that results are saved to a JSON file

Type the `set` command, Hit 'Enter' then choose `output_type` and hit 'Enter'. You will be displayed with a list of options for output. Choose `json_file`. You will then be prompted for a directory to which the output files will be saved.

    t>>> set
    [?] Perform action: output_type
    display_settings
    jwt
    output_dir
    > output_type
    username

    [?] Set output type: json_file
    raw
    table
    file
    > json_file

    ✓ Output type set to 'json_file'
    *Choose a directory for output files: ~/results
    ✓ Output directoy set to '~/results'

### Step 7: Run the 'getSystems' operation on the 'systems' api once again

Since we know we want to work with the Systems API, we can skip the first prompt by typing `systems` and hitting 'Enter' to get the list of operations for that API.

Follow the same steps as before to complete the call:

    t>>> systems
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
    ✓ Results saved to file: ~/results/1684788941328911.systems.getSystems.json

The filename for the file that contains the results for this operation will be displayed on the screen once completed.

    ✓ Results saved to file: ~/results/1684788941328911.systems.getSystems.json

The first part of the filename is a timestamp. The second and third part of the name are the API and operation id, respectively










