# CobraOS Deployment Guide

Deploy the full Cobra ecosystem to a Linux VPS, turning it into **CobraOS**.

---

## Prerequisites

- A VPS running **Ubuntu Server 22.04+** (or any Debian-based distro)
- **SSH access** with key-based authentication
- A domain or IP address pointing to the VPS

---

## Quick Deploy

```bash
# From the project root
./scripts/deploy.sh root@your-server-ip
```

This script:
1. Installs Python 3, git, GCC, and build tools
2. Clones the Cobra repo to `/opt/cobra`
3. Installs Cobra via `pip install -e .`
4. Creates the `cobra-shell` wrapper and adds it to `/etc/shells`
5. Installs the CobraOS `neofetch` command
6. Adds a login banner that runs `cobraos-init.cobra`

### Step-by-Step Deploy

#### 1. Install Dependencies

```bash
ssh root@your-server-ip
apt-get update
apt-get install -y python3 python3-pip git gcc make
```

#### 2. Clone and Install Cobra

```bash
git clone https://github.com/Amitk003/Cobra.git /opt/cobra
cd /opt/cobra
pip3 install -e .
```

#### 3. Set Up the Cobra Shell

```bash
# Create wrapper script
cat > /usr/local/bin/cobra-shell << 'EOF'
#!/bin/bash
exec python3 -m cobra.cli.cobra "$@"
EOF
chmod +x /usr/local/bin/cobra-shell

# Register as a valid login shell
echo '/usr/local/bin/cobra-shell' >> /etc/shells
```

#### 4. Change Default Shell

```bash
# For a specific user
chsh -s /usr/local/bin/cobra-shell username

# Or for root
chsh -s /usr/local/bin/cobra-shell
```

#### 5. Install neofetch

```bash
cat > /usr/local/bin/neofetch << 'EOF'
#!/bin/bash
cd /opt/cobra
python3 -m cobra.cli.cobra examples/neofetch.cobra
EOF
chmod +x /usr/local/bin/neofetch
```

#### 6. Set Up Login Banner

```bash
echo 'python3 -m cobra.cli.cobra /opt/cobra/examples/cobraos-init.cobra 2>/dev/null' >> ~/.bashrc
```

---

## SSH Tunnel

Access services on your VPS through a secure tunnel.

```bash
# Forward localhost:8080 -> VPS:80
./scripts/tunnel.sh root@your-server-ip

# Custom ports
./scripts/tunnel.sh root@your-server-ip 9090 3000
```

Or manually:

```bash
ssh -L 8080:localhost:80 -N -f root@your-server-ip
```

Now open `http://localhost:8080` in your browser to access the VPS service.

---

## Verification

SSH into your VPS:

```bash
ssh root@your-server-ip
```

You should see:

```
  ╔══════════════════════════════════════╗
  ║        CobraOS v0.1.0               ║
  ║  Building the future, one layer     ║
  ║  at a time.                         ║
  ╚══════════════════════════════════════╝

  Welcome, root!
  Login time: 2026-06-19T16:00:00.000000
  Hostname: your-server
```

Test the toolchain:

```bash
cobra --version
cobrac --help
cobrapkg list
cobraos neofetch
```

---

## Programmatic Deployment

```bash
# Using the Python deployment module
python -m cobra.os.deploy root@your-server-ip
```

This runs all deployment steps automatically via SSH.

---

## Architecture

```
[Phone/Tablet]          [Your Machine]              [VPS]
     │                       │                         │
     │   SSH Tunnel          │      CobraOS            │
     ├───────────────────────┼─────────────────────────┤
     │                       │                         │
     │   SSH Client  ────────┼─────── SSH Server       │
     │                       │         │               │
     │                       │    cobra-shell           │
     │                       │         │               │
     │                       │    cobra REPL            │
     │                       │         │               │
     │                       │    cobrac / cobrapkg     │
     │                       │                         │
```
