#!/bin/bash
cd /home/kavia/workspace/code-generation/fasteventapi-114770-348f66b2/event_manager_api_backend_workspace/event_manager_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

