#!/bin/bash
# CobraOS — SSH Tunnel Setup
# Creates a reverse tunnel so you can access your VPS from anywhere
#
# Usage:
#   ./scripts/tunnel.sh <user@host>          # Forward localhost:8080 -> VPS:80
#   ./scripts/tunnel.sh <user@host> 3000     # Custom local port
#   ./scripts/tunnel.sh <user@host> 8080 22  # Custom ports

set -e

HOST="$1"
LOCAL_PORT="${2:-8080}"
REMOTE_PORT="${3:-80}"

if [ -z "$HOST" ]; then
    echo "Usage: $0 <user@host> [local-port] [remote-port]"
    echo "Example: $0 root@123.456.789.0 9090 3000"
    exit 1
fi

echo "=== CobraOS Tunnel ==="
echo "Creating tunnel: localhost:$LOCAL_PORT -> $HOST -> localhost:$REMOTE_PORT"
echo ""
echo "Press Ctrl+C to close the tunnel."

ssh -L "$LOCAL_PORT:localhost:$REMOTE_PORT" -N "$HOST"

echo "Tunnel closed."
