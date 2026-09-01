#!/usr/bin/env python3
"""Command Line Interface for architecture-as-code-skills plugin."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_assets_root() -> tuple[Path, Path, Path]:
    """Locate skills, rules, and plugin.json from package or repository."""
    # Check if installed inside package directory
    pkg_dir = Path(__file__).resolve().parent
    if (pkg_dir / "skills").is_dir():
        skills_dir = pkg_dir / "skills"
        rules_dir = pkg_dir / "rules"
        plugin_file = pkg_dir / "plugin.json"
        return skills_dir, rules_dir, plugin_file

    # Fall back to repo root (when running in git clone)
    repo_root = pkg_dir.parent.parent
    skills_dir = repo_root / "skills"
    rules_dir = repo_root / "rules"
    plugin_file = repo_root / "plugin.json"

    if not skills_dir.is_dir():
        raise FileNotFoundError(
            f"Could not locate skills directory in {pkg_dir} or {repo_root}"
        )
    return skills_dir, rules_dir, plugin_file


def copy_or_link(src: Path, dst: Path, link: bool = False):
    """Copy or symlink a file or directory."""
    if dst.exists() or dst.is_symlink():
        if dst.is_dir() and not dst.is_symlink():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    dst.parent.mkdir(parents=True, exist_ok=True)
    if link:
        dst.symlink_to(src.resolve(), target_is_directory=src.is_dir())
    else:
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def find_c4_destination(repo_root: Path) -> str:
    """Find C4_DESTINATION from .env.dev or return default."""
    env_file = repo_root / ".env.dev"
    if env_file.is_file():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("C4_DESTINATION="):
                dest = line.split("=", 1)[1].strip().strip('"').strip("'")
                if dest:
                    return dest
    # Check common folders
    for candidate in ["docs/architecture", "structurizr_data", "structurizr"]:
        if (repo_root / candidate / "workspace.dsl").is_file():
            return candidate
    return "docs/architecture"


def handle_install(args):
    """Install skills and rules into the specified target environment."""
    skills_dir, rules_dir, plugin_file = get_assets_root()
    cwd = Path.cwd()
    home = Path.home()
    target = args.target.lower()
    is_global = args.global_install
    link = args.link

    print(f"Installing Architecture-as-Code skills (Target: {target}, Global: {is_global})...")

    if target in ("agents", "antigravity"):
        if is_global:
            dest = home / ".gemini" / "config" / "plugins" / "architecture-as-code"
        else:
            dest = cwd / ".agents" / "plugins" / "architecture-as-code"

        dest.mkdir(parents=True, exist_ok=True)
        copy_or_link(skills_dir, dest / "skills", link=link)
        if rules_dir.is_dir():
            copy_or_link(rules_dir, dest / "rules", link=link)
        if plugin_file.is_file():
            copy_or_link(plugin_file, dest / "plugin.json", link=link)

        print(f"✓ Installed Antigravity plugin to: {dest}")
        print("  Skills included: arch-c4-init, arch-c4-update")
        if rules_dir.is_dir():
            print("  Rules included: c4-dsl-standards, architecture-sync")

    elif target in ("claude", "claudecode"):
        if is_global:
            dest = home / ".claude" / "skills"
        else:
            dest = cwd / ".claude" / "skills"

        dest.mkdir(parents=True, exist_ok=True)
        for skill_folder in skills_dir.iterdir():
            if skill_folder.is_dir():
                copy_or_link(skill_folder, dest / skill_folder.name, link=link)

        print(f"✓ Installed Claude Code skills to: {dest}")
        for skill_folder in skills_dir.iterdir():
            if skill_folder.is_dir():
                print(f"  - {skill_folder.name}")

    elif target in ("cursor", "windsurf"):
        if is_global:
            dest = home / ".cursor" / "rules"
        else:
            dest = cwd / ".cursor" / "rules"

        dest.mkdir(parents=True, exist_ok=True)
        if rules_dir.is_dir():
            for rule_file in rules_dir.glob("*.md"):
                copy_or_link(rule_file, dest / rule_file.name, link=link)

        # Also copy skills to a local tools directory
        skills_dest = cwd / ".cursor" / "skills"
        skills_dest.mkdir(parents=True, exist_ok=True)
        copy_or_link(skills_dir, skills_dest, link=link)

        print(f"✓ Installed Cursor rules to: {dest}")
        print(f"✓ Installed Cursor skills reference to: {skills_dest}")

    elif target == "custom":
        if not args.path:
            sys.exit("Error: --path is required when using --target custom")
        dest = Path(args.path).resolve()
        dest.mkdir(parents=True, exist_ok=True)
        copy_or_link(skills_dir, dest / "skills", link=link)
        if rules_dir.is_dir():
            copy_or_link(rules_dir, dest / "rules", link=link)
        if plugin_file.is_file():
            copy_or_link(plugin_file, dest / "plugin.json", link=link)

        print(f"✓ Installed skills and rules to: {dest}")
    else:
        sys.exit(f"Error: Unknown target '{target}'. Supported: agents, claude, cursor, custom")


def handle_serve(args):
    """Launch Structurizr Local Docker container."""
    cwd = Path.cwd()
    dest = args.destination or find_c4_destination(cwd)
    dest_path = (cwd / dest).resolve()

    if not dest_path.is_dir():
        print(f"Warning: Destination folder '{dest_path}' does not exist yet.")
        dest_path.mkdir(parents=True, exist_ok=True)

    port = args.port
    print(f"Starting Structurizr Local on http://localhost:{port}")
    print(f"Mounting: {dest_path} -> /usr/local/structurizr")

    cmd = [
        "docker", "run", "-it", "--rm",
        "-p", f"{port}:8080",
        "-v", f"{dest_path}:/usr/local/structurizr",
        "structurizr/structurizr", "local"
    ]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        sys.exit("Error: Docker is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Structurizr container exited with error: {e}")


def handle_validate(args):
    """Validate Structurizr DSL files using Docker."""
    cwd = Path.cwd()
    dest = args.destination or find_c4_destination(cwd)
    dest_path = (cwd / dest).resolve()
    dsl_file = dest_path / "workspace.dsl"

    if not dsl_file.is_file():
        sys.exit(f"Error: Could not find workspace.dsl in '{dest_path}'")

    print(f"Validating Structurizr DSL in: {dest_path}")
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{dest_path}:/usr/local/structurizr",
        "structurizr/structurizr", "validate", "-w", "workspace.dsl"
    ]
    try:
        res = subprocess.run(cmd, check=True)
        print("✓ Structurizr DSL is valid.")
    except FileNotFoundError:
        sys.exit("Error: Docker is not installed or not in PATH.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Validation failed (exit code {e.returncode}).")


def main():
    parser = argparse.ArgumentParser(
        prog="arch-c4",
        description="Architecture-as-Code Toolkit & Agent Skills Manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # install subcommand
    install_parser = subparsers.add_parser("install", help="Install skills and rules into an agent environment")
    install_parser.add_argument(
        "-t", "--target",
        choices=["agents", "antigravity", "claude", "cursor", "custom"],
        default="agents",
        help="Target agent tool environment (default: agents / Antigravity)"
    )
    install_parser.add_argument(
        "-g", "--global",
        dest="global_install",
        action="store_true",
        help="Install globally for all projects on this machine"
    )
    install_parser.add_argument(
        "-p", "--path",
        help="Custom destination path (used with --target custom)"
    )
    install_parser.add_argument(
        "-l", "--link",
        action="store_true",
        help="Create symlinks instead of copying files"
    )

    # serve subcommand
    serve_parser = subparsers.add_parser("serve", help="Launch Structurizr Local via Docker")
    serve_parser.add_argument(
        "-d", "--destination",
        help="Path to folder containing workspace.dsl (defaults to C4_DESTINATION or docs/architecture)"
    )
    serve_parser.add_argument(
        "-p", "--port",
        default="8080",
        help="Host port to bind Structurizr web UI (default: 8080)"
    )

    # validate subcommand
    validate_parser = subparsers.add_parser("validate", help="Validate Structurizr DSL syntax")
    validate_parser.add_argument(
        "-d", "--destination",
        help="Path to folder containing workspace.dsl (defaults to C4_DESTINATION or docs/architecture)"
    )

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "install":
        handle_install(args)
    elif args.command == "serve":
        handle_serve(args)
    elif args.command == "validate":
        handle_validate(args)


if __name__ == "__main__":
    main()
