"""CobraOS — Deployment utilities for deploying to a VPS."""

import os
import sys
import subprocess
from pathlib import Path


def run_ssh(host: str, cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["ssh", host, cmd],
        capture_output=True, text=True, check=False
    )


def run_scp(host: str, local: str, remote: str):
    subprocess.run(
        ["scp", local, f"{host}:{remote}"],
        check=True
    )


def deploy_project(host: str, project_dir: str = "/opt/cobra"):
    print(f"Deploying Cobra to {host}:{project_dir}")
    run_ssh(host, f"mkdir -p {project_dir}")
    run_ssh(host, f"git clone https://github.com/Amitk003/Cobra.git {project_dir}")
    run_ssh(host, f"cd {project_dir} && pip install -e .")


def install_deps(host: str):
    print("Installing system dependencies...")
    run_ssh(host, "apt-get update -qq && apt-get install -y -qq python3 python3-pip git gcc")


def setup_shell(host: str):
    print("Setting up Cobra shell as login shell...")
    wrapper = """#!/bin/bash
exec python3 -m cobra.cli.cobra "$@"
"""
    run_ssh(host, "cat > /tmp/cobra-shell << 'EOF'\n" + wrapper + "\nEOF")
    run_ssh(host, "chmod +x /tmp/cobra-shell && mv /tmp/cobra-shell /usr/local/bin/")
    run_ssh(host, "grep -q '/usr/local/bin/cobra-shell' /etc/shells || echo '/usr/local/bin/cobra-shell' >> /etc/shells")


def setup_neofetch(host: str, project_dir: str = "/opt/cobra"):
    print("Setting up CobraOS neofetch...")
    neo = f"""#!/bin/bash
cd {project_dir}
python3 -m cobra.cli.cobrac examples/neofetch.cobra
"""
    run_ssh(host, f"cat > /usr/local/bin/neofetch << 'EOF'\n{neo}\nEOF")
    run_ssh(host, "chmod +x /usr/local/bin/neofetch")


def setup_banner(host: str, project_dir: str = "/opt/cobra"):
    print("Setting up login banner...")
    run_ssh(host, f"echo 'python3 -m cobra.cli.cobrac {project_dir}/examples/cobraos-init.cobra 2>/dev/null' >> ~/.bashrc")


def setup_tunnel(host: str, local_port: int = 8080, remote_port: int = 80):
    print(f"Setting up SSH tunnel: localhost:{local_port} -> {host}:{remote_port}")
    # Returns the command to run
    cmd = f"ssh -L {local_port}:localhost:{remote_port} -N -f {host}"
    print(f"Run: {cmd}")
    return cmd


def full_deploy(host: str):
    """Run all deployment steps."""
    install_deps(host)
    deploy_project(host)
    setup_shell(host)
    setup_neofetch(host)
    setup_banner(host)
    print("CobraOS deployment complete!")
    print(f"SSH into your VPS: ssh {host}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m cobra.os.deploy <user@host>")
        sys.exit(1)
    full_deploy(sys.argv[1])
