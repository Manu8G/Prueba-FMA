#!/bin/bash
set -e # Exit with nonzero exit code if anything fails
set -x # Print commands as they are executed

# switch
case "$1" in
"run-dev")
    # run dev
    uvicorn src.main:app --host 0.0.0.0 --port 80 --reload
    ;;
*) # run other
  exec "$@"
  ;;
esac
