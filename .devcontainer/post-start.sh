#!/bin/sh
# Plugin specific post-start.sh script.

CFG_FILE="./.devcontainer/pretalx.cfg"
TEMPLATE_FILE="./.devcontainer/pretalx.cfg.template"

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
RESET="\033[0m"

echo "${YELLOW}ℹ Current working directory: $(pwd)${RESET}"

if [ -f "$CFG_FILE" ]; then
  echo "${GREEN}✔ Configuration file '$CFG_FILE' already exists.${RESET}"
else
  if [ -f "$TEMPLATE_FILE" ]; then
    cp "$TEMPLATE_FILE" "$CFG_FILE"
    echo "${GREEN}⚡ Created '$CFG_FILE' from template.${RESET}"
  else
    echo "${RED}✖ Template file '$TEMPLATE_FILE' not found. Cannot create '$CFG_FILE'.${RESET}"
    exit 1
  fi
fi

