#!/bin/bash

# Variables
COMMAND=$1          # The command to run (passed as the first argument)
SEARCH_STRING=$2    # The string to search for in the output (passed as the second argument)
SLEEP_INTERVAL=0    # Time to wait between each iteration (in seconds)

# Check if the required arguments are provided
if [ -z "$COMMAND" ] || [ -z "$SEARCH_STRING" ]; then
  echo "Usage: $0 <command> <search_string>"
  exit 1
fi

# Loop until the command's output contains the search string
while true; do
  # Run the command and capture its output
  OUTPUT=$($COMMAND 2>&1)

  LOOP_COUNT=$((LOOP_COUNT + 1))


  # Check if the output contains the search string
  if echo "$OUTPUT" | grep -q "$SEARCH_STRING"; then
    echo "Found string '$SEARCH_STRING' in output. Exiting."
    # Print the command's output to the terminal
    echo "$OUTPUT"
    break
  fi

  echo "Finished with game: $LOOP_COUNT"

  # Wait for a specified interval before running the command again
  sleep $SLEEP_INTERVAL
done
