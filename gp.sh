#!/bin/bash
# Check if a commit message was provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <commit-message>" # Display usage if the commit message is missing
    exit 1                            # Exit the script with an error status
fi

# Store the commit message in a variable
COMMIT_MESSAGE="$1"

# Add all changes (tracked, new, and modified files) to the staging area
git add .

# Commit the changes with the provided commit message
git commit -m "$COMMIT_MESSAGE"

# Check if the commit was successful before attempting to push
if [ $? -eq 0 ]; then
    # Push the committed changes to the remote repository
    git push
else
    # Exit with code 1 if an error occurs.
    echo "Commit failed. Please check your changes and try again."
    exit 1
fi
