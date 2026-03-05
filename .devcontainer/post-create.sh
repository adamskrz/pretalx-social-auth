#!/bin/sh
# Plugin specific post-create.sh script.
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

echo "${YELLOW}ℹ Current working directory: $(pwd)${RESET}"
echo "${YELLOW}ℹ Initalizing pretalx.${RESET}"
echo "------"
python3 -m pretalx init --no-input
echo "------"
echo "${GREEN}✅ Pretalx initialized.${RESET}"

echo "${YELLOW}ℹ Collecting static files.${RESET}"
echo "-----"
python3 -m pretalx collectstatic --noinput
echo "-----"
echo "${GREEN}✅ Static files collected.${RESET}"

echo "${YELLOW}ℹ Create dummy event.${RESET}"
echo "-----"
python3 -m pretalx create_test_event
echo "-----"
echo "${GREEN}✅ Dummy event created ${RESET}"


# Finsih with a non-zero exit code to run default post-create.sh script.
# In every other case, please ensure proper error handling to avoid failing with a non-zero exit code.
exit 1;
