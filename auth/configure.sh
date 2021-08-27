#! bin/bash

config_file=./.configs/tacc_credentials.txt

function create_tacc_credentials() {
    printf "\nTACC Cloud credentials not found.\nProvide TACC username and password.\n"
    echo -n "Continue? [y/n]: "

    read choice

    if [[ $choice == "y" ]]; then
        # Create credentials.
        # If credential creation errors, exit with non-zero value
        echo -n "Username: "
        read username;
        echo -n "Password 🔒: "
        read -s password;
        printf "\n\n✓ TACC credentials created successfully\n\n"

        echo "TACC_USERNAME=${username}" > "${config_file}"
        echo "TACC_PASSWORD=${password}" >> "${config_file}"

        return;
    fi

    exit 1
}

. "${config_file}"

if [[ -z "$TACC_USERNAME" ]] || [[ -z "$TACC_PASSWORD" ]]; then
    create_tacc_credentials
    exit
fi

exit