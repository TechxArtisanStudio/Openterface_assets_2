#!/usr/bin/env python3
"""
Interactive setup script for static-assets-template
This script helps you configure the template for your GitHub repository.
"""

import os
import sys
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple, List

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def validate_github_username(username: str) -> bool:
    """Validate GitHub username format."""
    if not username:
        return False
    # GitHub usernames: alphanumeric and hyphens, 1-39 characters
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$'
    return bool(re.match(pattern, username))


def validate_repo_name(repo_name: str) -> bool:
    """Validate repository name format."""
    if not repo_name:
        return False
    # Repository names: alphanumeric, hyphens, underscores, dots, 1-100 characters
    pattern = r'^[a-zA-Z0-9._-]{1,100}$'
    return bool(re.match(pattern, repo_name))


def parse_github_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse GitHub repository URL and extract username and repository name.
    Supports formats:
    - https://github.com/username/repo-name
    - https://github.com/username/repo-name.git
    - git@github.com:username/repo-name.git
    - github.com/username/repo-name
    
    Returns: (username, repo_name) or (None, None) if invalid
    """
    url = url.strip()
    
    # Remove trailing .git if present
    if url.endswith('.git'):
        url = url[:-4]
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Pattern for GitHub URLs
    patterns = [
        r'https?://github\.com/([^/]+)/([^/]+)',  # HTTPS
        r'git@github\.com:([^/]+)/([^/]+)',       # SSH
        r'github\.com/([^/]+)/([^/]+)',            # Without protocol
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            username = match.group(1)
            repo_name = match.group(2)
            
            # Validate extracted values
            if validate_github_username(username) and validate_repo_name(repo_name):
                return username, repo_name
    
    return None, None


def get_github_repo_url() -> Tuple[str, str]:
    """Prompt for GitHub repository URL and extract username and repo name."""
    print_info("Enter your GitHub repository URL.")
    print_info("Examples:")
    print(f"  {Colors.OKCYAN}https://github.com/username/repo-name{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}https://github.com/username/repo-name.git{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}git@github.com:username/repo-name.git{Colors.ENDC}")
    print()
    
    while True:
        url = input(f"{Colors.OKCYAN}GitHub repository URL: {Colors.ENDC}").strip()
        
        if not url:
            print_error("URL cannot be empty. Please try again.")
            continue
        
        username, repo_name = parse_github_url(url)
        
        if not username or not repo_name:
            print_error("Invalid GitHub repository URL format.")
            print_info("Accepted formats:")
            print("  - https://github.com/username/repo-name")
            print("  - https://github.com/username/repo-name.git")
            print("  - git@github.com:username/repo-name.git")
            print("  - github.com/username/repo-name")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                sys.exit(1)
            continue
        
        return username, repo_name


def check_git_config(project_root: Optional[Path] = None) -> Tuple[bool, Optional[str], Optional[str]]:
    """Check if git user.name and user.email are configured.
    Returns: (is_configured, user_name, user_email)
    """
    try:
        if project_root is None:
            project_root = Path(__file__).parent
        
        # Check global config first
        name_result = subprocess.run(
            ['git', 'config', '--global', 'user.name'],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False
        )
        email_result = subprocess.run(
            ['git', 'config', '--global', 'user.email'],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False
        )
        
        user_name = name_result.stdout.strip() if name_result.returncode == 0 else None
        user_email = email_result.stdout.strip() if email_result.returncode == 0 else None
        
        if user_name and user_email:
            return True, user_name, user_email
        
        # Check local config if global not set
        if (project_root / '.git').exists():
            name_result = subprocess.run(
                ['git', 'config', 'user.name'],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )
            email_result = subprocess.run(
                ['git', 'config', 'user.email'],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )
            
            user_name = name_result.stdout.strip() if name_result.returncode == 0 else None
            user_email = email_result.stdout.strip() if email_result.returncode == 0 else None
            
            if user_name and user_email:
                return True, user_name, user_email
        
        return False, user_name, user_email
    except FileNotFoundError:
        return False, None, None


def configure_git_user(project_root: Path, set_global: bool = False) -> bool:
    """Prompt user for git user.name and user.email and configure them."""
    print_warning("Git user identity is not configured.")
    print_info("Git requires your name and email for commits.")
    
    user_name = input(f"{Colors.OKCYAN}Enter your name (for git commits): {Colors.ENDC}").strip()
    if not user_name:
        print_error("Name cannot be empty.")
        return False
    
    user_email = input(f"{Colors.OKCYAN}Enter your email (for git commits): {Colors.ENDC}").strip()
    if not user_email:
        print_error("Email cannot be empty.")
        return False
    
    # Validate email format (basic check)
    if '@' not in user_email:
        print_warning("Email format looks invalid, but continuing anyway...")
    
    try:
        scope = '--global' if set_global else '--local'
        
        subprocess.run(
            ['git', 'config', scope, 'user.name', user_name],
            cwd=project_root,
            check=True
        )
        subprocess.run(
            ['git', 'config', scope, 'user.email', user_email],
            cwd=project_root,
            check=True
        )
        
        print_success(f"Git user configured: {user_name} <{user_email}>")
        if set_global:
            print_info("(Set globally - will be used for all repositories)")
        else:
            print_info("(Set locally - only for this repository)")
        
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to configure git user: {e}")
        return False


def check_ssh_keys() -> bool:
    """Check if SSH keys exist (doesn't verify GitHub connection)."""
    try:
        # Check for SSH keys in common locations
        ssh_dir = Path.home() / '.ssh'
        if not ssh_dir.exists():
            return False
        
        # Check for common SSH key files
        ssh_key_files = ['id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa']
        for key_file in ssh_key_files:
            # Check for private key or public key
            if (ssh_dir / key_file).exists() or (ssh_dir / f"{key_file}.pub").exists():
                return True
        
        return False
    except Exception:
        return False


def get_remote_preference() -> str:
    """Ask user for remote URL preference (SSH or HTTPS)."""
    print()
    print_info("Choose how to connect to GitHub:")
    print("  [1] SSH (git@github.com) - Recommended if you have SSH keys configured")
    print("  [2] HTTPS (https://github.com) - Requires username/password or token")
    
    has_ssh = check_ssh_keys()
    if has_ssh:
        print(f"   {Colors.OKGREEN}✓ SSH keys detected{Colors.ENDC}")
        default = "1"
    else:
        print(f"   {Colors.WARNING}⚠ No SSH keys detected{Colors.ENDC}")
        default = "2"
    
    while True:
        choice = input(f"{Colors.OKCYAN}Choose [1/2] (default: {default}): {Colors.ENDC}").strip()
        if not choice:
            choice = default
        
        if choice == "1":
            return "ssh"
        elif choice == "2":
            return "https"
        else:
            print_error("Invalid choice. Please enter 1 or 2.")


def get_remote_url(username: str, repo_name: str, remote_type: str = "ssh") -> str:
    """Generate remote URL based on type."""
    if remote_type == "ssh":
        return f"git@github.com:{username}/{repo_name}.git"
    else:
        return f"https://github.com/{username}/{repo_name}.git"


def get_destination_path(repo_name: str, default_path: Path) -> Path:
    """Prompt user for destination path, with default option.
    Returns the destination path (default or custom).
    """
    print()
    print_info("Enter destination path (press Enter for default):")
    print(f"  Default: {Colors.OKCYAN}{default_path}{Colors.ENDC}")
    print()
    
    while True:
        path_input = input(f"{Colors.OKCYAN}Destination path [{default_path}]: {Colors.ENDC}").strip()
        
        # If empty, use default
        if not path_input:
            return default_path
        
        # Process custom path
        try:
            custom_path = Path(path_input).expanduser().resolve()
            
            # If path is a directory, append repo_name
            if custom_path.is_dir():
                custom_path = custom_path / repo_name
            # If path doesn't exist but parent does, use it as-is
            elif not custom_path.exists() and custom_path.parent.exists():
                pass  # Use as-is
            # If path doesn't exist and parent doesn't exist, ask to create
            elif not custom_path.parent.exists():
                create = input(f"{Colors.WARNING}Parent directory doesn't exist. Create it? (y/n): {Colors.ENDC}").strip().lower()
                if create == 'y':
                    try:
                        custom_path.parent.mkdir(parents=True, exist_ok=True)
                        print_success(f"Created directory: {custom_path.parent}")
                    except Exception as e:
                        print_error(f"Failed to create directory: {e}")
                        retry = input("Try again? (y/n): ").strip().lower()
                        if retry != 'y':
                            return default_path
                        continue
                else:
                    retry = input("Try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        return default_path
                    continue
            
            return custom_path
        except Exception as e:
            print_error(f"Invalid path: {e}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return default_path
            continue


def copy_template_folder(repo_name: str, destination_path: Path) -> Optional[Path]:
    """Copy the template folder to a new location with the repository name.
    Excludes .git directory from the copy.
    
    Args:
        repo_name: Name of the repository
        destination_path: Destination path for the new project folder.
    
    Returns the new project root path if successful, None otherwise.
    """
    template_project_root = Path(__file__).parent
    new_folder_path = destination_path
    
    # Check if target folder already exists
    if new_folder_path.exists():
        print_warning(f"Folder already exists at: {new_folder_path}")
        overwrite = input(f"{Colors.WARNING}Do you want to overwrite it? (y/n): {Colors.ENDC}").strip().lower()
        if overwrite != 'y':
            print_info("Setup cancelled. Please choose a different path or remove the existing folder.")
            return None
        # Remove existing folder
        try:
            shutil.rmtree(new_folder_path)
            print_info(f"Removed existing folder: {new_folder_path}")
        except Exception as e:
            print_error(f"Failed to remove existing folder: {e}")
            return None
    
    try:
        print_info(f"Copying template folder...")
        print_info(f"Source: {template_project_root}")
        print_info(f"Destination: {new_folder_path}")
        
        # Copy the entire folder, excluding .git
        def ignore_git(dirname, filenames):
            """Ignore .git directory and its contents."""
            ignored = []
            if '.git' in filenames:
                ignored.append('.git')
            return ignored
        
        shutil.copytree(
            template_project_root,
            new_folder_path,
            ignore=ignore_git,
            dirs_exist_ok=False
        )
        
        print_success(f"Template folder copied successfully!")
        print_info(f"New project path: {new_folder_path}")
        
        # Change to the new directory
        os.chdir(new_folder_path)
        print_info(f"Changed working directory to: {new_folder_path}")
        
        return new_folder_path
    except PermissionError:
        print_error("Permission denied. Cannot copy folder.")
        print_info("You may need to close any programs using this folder.")
        return None
    except Exception as e:
        print_error(f"Failed to copy folder: {e}")
        return None


def update_config_toml(username: str, repo_name: str, project_root: Optional[Path] = None) -> bool:
    """Update config.toml with the provided GitHub Pages URL."""
    if project_root is None:
        project_root = Path(__file__).parent
    config_path = project_root / 'config.toml'
    
    if not config_path.exists():
        print_error("config.toml not found in project root!")
        return False
    
    base_url = f"https://{username}.github.io/{repo_name}"
    
    try:
        # Read current config
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update base_url
        pattern = r'base_url\s*=\s*"[^"]*"'
        replacement = f'base_url = "{base_url}"'
        content = re.sub(pattern, replacement, content)
        
        # Update domain (set to empty for project sites)
        pattern = r'domain\s*=\s*"[^"]*"'
        replacement = 'domain = ""'
        content = re.sub(pattern, replacement, content)
        
        # Write updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success(f"Updated config.toml with base_url: {base_url}")
        return True
    
    except Exception as e:
        print_error(f"Failed to update config.toml: {e}")
        return False


def generate_git_commands(username: str, repo_name: str, project_root: Path, remote_type: str = "ssh") -> List[str]:
    """Generate git commands for the user to run."""
    commands = []
    
    remote_url = get_remote_url(username, repo_name, remote_type)
    
    # Since we're working in a copy (without .git), always initialize fresh
    if (project_root / '.git').exists():
        print_info("Git repository already initialized in copy.")
        # Check if remote exists
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                existing_remote = result.stdout.strip()
                expected_remote_https = f"https://github.com/{username}/{repo_name}.git"
                expected_remote_ssh = f"git@github.com:{username}/{repo_name}.git"
                # Check if remote matches expected (either HTTPS or SSH format)
                if (expected_remote_https not in existing_remote and 
                    expected_remote_ssh not in existing_remote and 
                    f"{username}/{repo_name}" not in existing_remote):
                    # Remote doesn't match, need to update it
                    commands.append(f"git remote set-url origin {remote_url}")
                else:
                    print_info(f"Remote origin already configured: {existing_remote}")
            else:
                commands.append(f"git remote add origin {remote_url}")
        except:
            commands.append(f"git remote add origin {remote_url}")
    else:
        # Initialize new git repository (copy doesn't have .git)
        commands.append("git init -b main")  # Initialize with 'main' branch
        commands.append("git add .")
        commands.append('git commit -m "Initial commit from static-assets-template"')
        commands.append(f"git remote add origin {remote_url}")
    
    # Only rename branch if needed (git init -b main already creates main branch)
    # For existing repos that might have 'master' branch, we'll rename it
    if (project_root / '.git').exists():
        # Check current branch name
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False
            )
            current_branch = result.stdout.strip() if result.returncode == 0 else None
            if current_branch and current_branch != 'main':
                commands.append("git branch -M main")
        except:
            pass
    
    commands.append(f"git push -u origin main")
    
    return commands


def main():
    """Main setup function."""
    print_header("Static Assets Template Setup")
    
    print_info("This script will help you configure the template for your GitHub repository.")
    print_info("You'll need:")
    print("  1. A GitHub account")
    print("  2. A new repository created on GitHub (or we'll help you create one)")
    print("  3. Your GitHub repository URL\n")
    
    # Get GitHub repository URL and parse it
    username, repo_name = get_github_repo_url()
    print_success(f"GitHub username: {username}")
    print_success(f"Repository name: {repo_name}")
    
    # Copy template folder to new location
    print_header("Creating Project Copy")
    template_project_root = Path(__file__).parent
    parent_dir = template_project_root.parent
    default_folder_path = parent_dir / repo_name
    
    print_info(f"Template folder: {Colors.OKCYAN}{template_project_root}{Colors.ENDC}")
    print()
    
    # Get destination path (default or custom)
    destination_path = get_destination_path(repo_name, default_folder_path)
    
    print()
    print_info(f"Destination: {Colors.OKCYAN}{destination_path}{Colors.ENDC}")
    print_info("The template folder will be copied to the destination.")
    print_info("The original template folder will remain unchanged.")
    print()
    
    new_project_root = copy_template_folder(repo_name, destination_path)
    if new_project_root is None:
        print_error("Failed to copy template folder. Setup cancelled.")
        sys.exit(1)
    
    # Update references to work in the new folder
    current_project_root = new_project_root
    
    # Confirm settings
    base_url = f"https://{username}.github.io/{repo_name}"
    repo_url = f"https://github.com/{username}/{repo_name}"
    print(f"\n{Colors.BOLD}Configuration Summary:{Colors.ENDC}")
    print(f"  GitHub Username: {Colors.OKGREEN}{username}{Colors.ENDC}")
    print(f"  Repository Name: {Colors.OKGREEN}{repo_name}{Colors.ENDC}")
    print(f"  Repository URL: {Colors.OKGREEN}{repo_url}{Colors.ENDC}\n")
    
    confirm = input(f"{Colors.WARNING}Is this correct? (y/n): {Colors.ENDC}").strip().lower()
    if confirm != 'y':
        print_info("Setup cancelled. Run the script again when ready.")
        sys.exit(0)
    
    # Update config.toml
    print_header("Updating Configuration")
    if not update_config_toml(username, repo_name, current_project_root):
        print_error("Failed to update configuration. Please check the error above.")
        sys.exit(1)
    
    # Generate URL links
    print_header("Generating Asset Links")
    generate_url_script = current_project_root / 'scripts' / 'generate_url.py'
    
    if not generate_url_script.exists():
        print_warning("generate_url.py script not found. Skipping link generation.")
    else:
        try:
            print_info("Generating markdown files with asset URLs...")
            result = subprocess.run(
                [sys.executable, str(generate_url_script)],
                cwd=current_project_root,
                check=False,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print_success("Asset links generated successfully!")
                print_info("Updated files in links/ directory with new URLs")
            else:
                print_warning("Link generation completed with warnings.")
                if result.stderr:
                    for line in result.stderr.strip().split('\n'):
                        if line.strip():
                            print(f"   {Colors.WARNING}{line}{Colors.ENDC}")
        except Exception as e:
            print_warning(f"Could not run generate_url.py: {e}")
            print_info("You can run it manually later: python scripts/generate_url.py")
    
    # Ask for remote preference (SSH or HTTPS)
    print_header("Git Remote Configuration")
    remote_type = get_remote_preference()
    remote_url_str = get_remote_url(username, repo_name, remote_type)
    print_success(f"Using {remote_type.upper()} remote: {remote_url_str}")
    
    # Verify we're in the copy (should not have .git)
    print_header("Git Repository Status")
    if (current_project_root / '.git').exists():
        print_warning("⚠️  WARNING: .git directory found in copy!")
        print_warning("This shouldn't happen. Removing .git directory...")
        try:
            shutil.rmtree(current_project_root / '.git')
            print_success("Removed .git directory from copy")
        except Exception as e:
            print_error(f"Failed to remove .git: {e}")
            print_warning("Please manually remove .git directory before continuing.")
    else:
        print_info("Working in fresh copy (no .git directory)")
    
    # Generate next steps
    print_header("Next Steps")
    
    print(f"{Colors.BOLD}1. Create GitHub Repository:{Colors.ENDC}")
    print(f"   Go to: {Colors.OKCYAN}https://github.com/new{Colors.ENDC}")
    print(f"   Repository name: {Colors.OKGREEN}{repo_name}{Colors.ENDC}")
    print(f"   DO NOT initialize with README, .gitignore, or license")
    print(f"   Click 'Create repository'\n")
    
    print(f"{Colors.BOLD}2. Initialize Git and Push:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}Note: The script can run these commands for you automatically.{Colors.ENDC}")
    git_commands = generate_git_commands(username, repo_name, current_project_root, remote_type)
    for i, cmd in enumerate(git_commands, 1):
        print(f"   {Colors.OKCYAN}{cmd}{Colors.ENDC}")
    print()
    
    # Ask if user wants to run git commands
    push_succeeded = False  # Track if push succeeded (for showing URLs later)
    
    if git_commands:
        run_git = input(f"{Colors.OKCYAN}Would you like to run the git commands now? (y/n): {Colors.ENDC}").strip().lower()
        if run_git == 'y':
            print_header("Running Git Commands")
            project_root = current_project_root
            
            # Check git user configuration before running commands
            is_git_configured, git_name, git_email = check_git_config(project_root)
            if not is_git_configured:
                print()
                set_global = input(f"{Colors.OKCYAN}Set git user globally (for all repos) or locally (this repo only)? (global/local) [local]: {Colors.ENDC}").strip().lower()
                set_global = set_global == 'global'
                
                if not configure_git_user(project_root, set_global=set_global):
                    print_error("Failed to configure git user. Please configure manually:")
                    print_info("  git config --global user.name 'Your Name'")
                    print_info("  git config --global user.email 'your.email@example.com'")
                    print_warning("Continuing with git commands, but commit may fail if user is not configured.")
                print()
            
            # Track if commit and push succeeded
            commit_succeeded = False
            should_skip_remaining = False
            
            for i, cmd in enumerate(git_commands):
                # Skip remaining commands if commit failed
                if should_skip_remaining:
                    if 'push' in cmd.lower():
                        print_warning(f"Skipping: {cmd}")
                        print_info("(Commit did not succeed, so push is skipped)")
                    continue
                
                print_info(f"Running: {cmd}")
                try:
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        cwd=project_root,
                        check=False,
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print_success(f"Command completed successfully")
                        # Check if this was a commit command
                        if 'commit' in cmd.lower():
                            commit_succeeded = True
                        # Check if this was a push command
                        if 'push' in cmd.lower():
                            push_succeeded = True
                    else:
                        print_warning(f"Command returned non-zero exit code.")
                        if result.stderr:
                            # Print error output
                            for line in result.stderr.strip().split('\n'):
                                if line.strip():
                                    print(f"   {Colors.FAIL}{line}{Colors.ENDC}")
                        
                        # If commit failed, skip remaining commands (especially push)
                        if 'commit' in cmd.lower():
                            commit_succeeded = False
                            should_skip_remaining = True
                            print_warning("Commit failed. Remaining commands will be skipped.")
                        elif 'push' in cmd.lower() and not commit_succeeded:
                            print_warning("Push skipped - commit did not succeed.")
                except Exception as e:
                    print_error(f"Error running command: {e}")
                    print_warning("Please run the commands manually.")
                    if 'commit' in cmd.lower():
                        should_skip_remaining = True
                    break
    
    print_header("Setup Complete!")
    print_success("Configuration has been updated successfully!")
    
    # Show GitHub Pages URL and test URLs if git push succeeded
    if push_succeeded:
        print()
        print(f"{Colors.BOLD}GitHub Pages URL:{Colors.ENDC}")
        print(f"   {Colors.OKGREEN}{base_url}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Test Your URLs:{Colors.ENDC}")
        print(f"   Sample image (JPG): {Colors.OKCYAN}{base_url}/images/sample.jpg{Colors.ENDC}")
        print(f"   Sample image (WebP): {Colors.OKCYAN}{base_url}/images/sample.webp{Colors.ENDC}")
        print(f"   Minified CSS: {Colors.OKCYAN}{base_url}/css/style.min.css{Colors.ENDC}")
        print(f"   Minified JS: {Colors.OKCYAN}{base_url}/js/app.min.js{Colors.ENDC}\n")
    
    # Show deployment wait step (only if push succeeded)
    if push_succeeded:
        print(f"{Colors.BOLD}Next: Wait for Deployment{Colors.ENDC}")
        print(f"   1. Go to: {Colors.OKCYAN}https://github.com/{username}/{repo_name}/actions{Colors.ENDC}")
        print(f"   2. Wait for 'Deploy to GitHub Pages' workflow to complete")
        print(f"      (This will create the 'gh-pages' branch)\n")
        
        print(f"{Colors.BOLD}3. {Colors.WARNING}⚠️  IMPORTANT - Configure GitHub Pages:{Colors.ENDC}")
        print(f"   {Colors.WARNING}This is a REQUIRED step for your site to work!{Colors.ENDC}")
        print(f"   {Colors.WARNING}Do this AFTER the workflow creates the 'gh-pages' branch.{Colors.ENDC}")
        print(f"   Go to: {Colors.OKCYAN}https://github.com/{username}/{repo_name}/settings/pages{Colors.ENDC}")
        print(f"   Under 'Source', select: {Colors.OKGREEN}Deploy from a branch{Colors.ENDC}")
        print(f"   Branch: {Colors.OKGREEN}gh-pages{Colors.ENDC}")
        print(f"   Folder: {Colors.OKGREEN}/(root){Colors.ENDC}")
        print(f"   {Colors.WARNING}Make sure to select 'gh-pages' branch (not 'main'){Colors.ENDC}\n")
        
        print(f"   4. Wait 2-5 minutes for GitHub Pages to propagate")
        print(f"   5. Your site will be available at: {Colors.OKGREEN}{base_url}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Troubleshooting:{Colors.ENDC}")
    print(f"   If you get 404 errors, check:")
    print(f"   - Verify workflow completed successfully")
    print(f"   - Check that 'gh-pages' branch exists: {Colors.OKCYAN}https://github.com/{username}/{repo_name}/tree/gh-pages{Colors.ENDC}")
    print(f"   - Verify GitHub Pages is set to 'gh-pages' branch (not 'main')")
    print(f"   - Wait a few minutes - GitHub Pages can take 2-5 minutes to update")
    print(f"   - Check if files exist in gh-pages branch: {Colors.OKCYAN}https://github.com/{username}/{repo_name}/tree/gh-pages/images{Colors.ENDC}\n")
    
    print_info("Follow the steps above to complete your GitHub Pages setup.")
    print_info(f"For detailed instructions, see: {Colors.OKCYAN}SETUP.md{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup cancelled by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        sys.exit(1)
