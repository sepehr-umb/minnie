#!/bin/bash
# This script helps users move through the Minnie Server project

# Colors
GREEN="\e[32m"
BLUE="\e[34m"
RESET="\e[0m"

# --- Integration setup ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STUDENT="${USER:-$(whoami)}"
export TUTOR_STATE_FILE="${SCRIPT_DIR}/json-backend/brains.json"
export TUTOR_PROJECT_DIR="${SCRIPT_DIR}/hello_project"

# Start watcher.py in the background
python3 "${SCRIPT_DIR}/watcher.py" --student "$STUDENT" &
WATCHER_PID=$!
# Kill watcher when tutor exits
trap "kill $WATCHER_PID 2>/dev/null" EXIT

# Helper: record completed command to backend
record() {
    python3 "${SCRIPT_DIR}/json-backend/backend.py" \
        --student "$STUDENT" --validate 0 --cmd "$1"
}
# ---

#This Script looks for exact matches for its string prompts to prevent malicious code from being injected.
#If modified for more lax prompting, ensure that strings are escaped properly.

usrPrompt() {
    local display_dir="${PWD/#$HOME/~}"
    printf "${GREEN}(Minnie)${BLUE} %s \$ ${RESET}" "$display_dir"
}

intro="Welcome to the Minnie Server, this project will help you gain experience with backend development."

find_helloproj="Let's begin by locating the hello project directory, use the command: cd hello_project/"

cmdERR="There was an issue with your command, check your spelling and try again."

prompt_user() {
    read -e -p "$(usrPrompt)" prompt
}

function verifyCD() {
 verified="false"
 while [ "$verified" == "false" ]; do
        if [ "$prompt" == "cd hello_project/" ]; then
                eval $prompt
                if [ "$PWD" == "$expectedPWD" ]; then
                 echo "You have successfully moved into the hello project directory!"
                 record "$prompt"
                 verified="true"

                else
                echo "$cmdERR"
                prompt_user
                continue
                fi
        else
                echo "$cmdERR"
                prompt_user
        fi
 done
}

function verifyPWD() {
        verified="false"
        while [ "$verified" == "false" ]; do
                if [ "$prompt" == "pwd" ]; then
                        verified="true"
                        eval $prompt
                        record "$prompt"
                else
                echo "$cmdERR"
                prompt_user
                fi
        done
}

function verifyListDir() {
	verified="false"
	while [ "$verified" == "false" ]; do
		if [ "$prompt" == "ls -l" ]; then
			verified="true"
			eval $prompt
			record "$prompt"
		else
		echo "$cmdERR"
		prompt_user
		fi
	done
}

#function validateDjango() {
#	#validate script integrity of script for security reasons, then run on directory.
#
#	#validate django files using python script
#}

function checkRegen() {
	if ["$prompt"  == "djangoRegen" ]; then
	regenScript
	fi
}

echo $intro
echo $find_helloproj

expectedPWD="$(cd "$(dirname "$0")" && pwd)/hello_project"

prompt_user
verifyCD

echo "You should now be in the hello project folder, you can verify this by using the pwd command, try it now."
echo

prompt_user
verifyPWD

echo
echo "Now that we've verified we are in the right place, let's explore the files in this directory."
echo "Using \"ls -l\" take a look at the files in this directory, then use the command \"cat <filename>\" To print the contents of a file."

prompt_user
verifyListDir

prompt_user
verifyCat

#Verify File integrity TODO: Move to script start
filesValidated=validateDjango

if [ filesValidated = "true" ]; then
	echo
	echo "Now it's time to get ready to make some changes on your own, \"nano views.py\" to open the nano text editor, then change the message in the view function."

	verifyNano
	filesValidated="false"
	python3 validateDjango.py
	status=$?
	filesValidated=status
	if [ "$filesValidated" == "true" ]; then
		: #Do something I guess
	else
		echo "Files are invalid, please rectify the file or consult an administrator for assistance."
		echo "Try modifying the file, or if issue persists, run command djangoReset to regenerate and replace project files."
		prompt_user
		checkRegen
		verifyNano
	fi
fi