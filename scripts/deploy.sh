#!/bin/bash
# CobraOS — VPS Deployment Script
# Usage: ./scripts/deploy.sh <user@host>
#
# Requirements:
#   - Ubuntu Server 22.04+ on the VPS
#   - SSH access with key-based auth
#   - Python 3.10+ installed on the VPS

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <user@host>"
    echo "Example: $0 root@123.456.789.0"
    exit 1
fi

HOST="$1"
PROJECT_DIR="/opt/cobra"

echo "=== CobraOS Deployment ==="
echo "Target: $HOST"
echo "Project dir: $PROJECT_DIR"
echo ""

# 1. System dependencies
echo "[1/6] Installing system dependencies..."
ssh "$HOST" "
    apt-get update -qq
    apt-get install -y -qq python3 python3-pip git curl gcc make neofetch 2>/dev/null
" || echo "Warning: Some packages may have failed"

# 2. Clone/update project
echo "[2/6] Deploying Cobra project..."
ssh "$HOST" "
    if [ -d '$PROJECT_DIR' ]; then
        cd '$PROJECT_DIR' && git pull
    else
        git clone https://github.com/Amitk003/Cobra.git '$PROJECT_DIR'
    fi
"

# 3. Install Cobra
echo "[3/6] Installing Cobra toolchain..."
ssh "$HOST" "cd '$PROJECT_DIR' && pip install -e ."

# 4. Install Cobra shell as login shell
echo "[4/6] Configuring Cobra shell..."
# Add /usr/local/bin/cobra to /etc/shells if not present
ssh "$HOST" "
    if ! grep -q '/usr/local/bin/cobra' /etc/shells 2>/dev/null; then
        # Create a wrapper script
        cat > /usr/local/bin/cobra-shell << 'WRAPPER'
#!/bin/bash
exec python3 -m cobra.cli.cobra \"\$@\"
WRAPPER
        chmod +x /usr/local/bin/cobra-shell
        echo '/usr/local/bin/cobra-shell' >> /etc/shells
    fi
"

# 5. Set up neofetch wrapper
echo "[5/6] Configuring CobraOS neofetch..."
ssh "$HOST" "
    cat > /usr/local/bin/neofetch << 'WRAPPER'
#!/bin/bash
cd '$PROJECT_DIR'
python3 -m cobra.cli.cobrac examples/neofetch.cobra
WRAPPER
    chmod +x /usr/local/bin/neofetch
"

# 6. Set up boot banner
echo "[6/6] Configuring login banner..."
ssh "$HOST" "
    # Add init message to .bashrc
    echo 'python3 -m cobra.cli.cobrac /opt/cobra/examples/cobraos-init.cobra 2>/dev/null' >> ~/.bashrc
"

echo ""
echo "=== Deployment complete! ==="
echo "SSH into your VPS: ssh $HOST"
echo ""
echo "To set Cobra as your default shell:"
echo "  ssh $HOST 'chsh -s /usr/local/bin/cobra-shell'"
echo ""
