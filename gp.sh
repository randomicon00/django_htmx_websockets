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

# Check for staged changes before committing
if git diff --cached --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Commit the changes with the provided commit message, checking success inline
if git commit -m "$COMMIT_MESSAGE"; then
    # Push the committed changes to the remote repository if commit succeeds
    git push
else
    echo "Commit failed. Please check your changes and try again."
    exit 1
fi
