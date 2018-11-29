#!/usr/bin/env bash
# Check token
if [[ ! "${1}" ]]; then
	echo "Error: no token specified"
	exit 1
fi

# Check email
if [[ ! "${2}" ]]; then
	echo "Error: no email specified"
	exit 1
fi

# Retrieve user information from slack api
USER_EMAIL=$(git show -s --pretty=%ce | tr -d '[:space:]')
URL="https://slack.com/api/users.lookupByEmail?token=${1}&email=${2}"
echo "$(curl -s "${URL}" | jq .user.name | tr -d \")"
