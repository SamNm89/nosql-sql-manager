#!/usr/bin/env python3
"""Deployment script for the Banking Management System."""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from logging_config import banking_logger

logger = banking_logger.get_logger("Deploy")

class Deployer:
    """Deployment manager for the banking application."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_name = "banking_env"
        
    def check_python_version(self):
        """Check if Python version is compatible."""
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required")
            sys.exit(1)
        logger.info(f"Python version {sys.version} is compatible")
    
    def create_virtual_environment(self):
        """Create a virtual environment."""
        venv_path = self.project_root / self.venv_name
        
        if venv_path.exists():
            logger.info("Virtual environment already exists")
            return venv_path
        
        logger.info("Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            logger.info("Virtual environment created successfully")
            return venv_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create virtual environment: {e}")
            sys.exit(1)
    
    def get_python_executable(self, venv_path):
        """Get the Python executable from virtual environment."""
        if os.name == "nt":  # Windows
            return venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            return venv_path / "bin" / "python"
    
    def get_pip_executable(self, venv_path):
        """Get the pip executable from virtual environment."""
        if os.name == "nt":  # Windows
            return venv_path / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            return venv_path / "bin" / "pip"
    
    def install_dependencies(self, venv_path):
        """Install project dependencies."""
        pip_executable = self.get_pip_executable(venv_path)
        
        logger.info("Installing dependencies...")
        try:
            # Upgrade pip first
            subprocess.run([str(pip_executable), "install", "--upgrade", "pip"], check=True)
            
            # Install requirements
            subprocess.run([str(pip_executable), "install", "-r", "requirements.txt"], check=True)
            
            # Install the package in development mode
            subprocess.run([str(pip_executable), "install", "-e", "."], check=True)
            
            logger.info("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            sys.exit(1)
    
    def create_directories(self):
        """Create necessary directories."""
        directories = ["logs", "backups", "exports"]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def create_config_file(self):
        """Create default configuration file if it doesn't exist."""
        config_file = self.project_root / "config.json"
        
        if not config_file.exists():
            logger.info("Creating default configuration file...")
            # The config will be created automatically when the app runs
            logger.info("Configuration file will be created on first run")
    
    def create_shortcut(self, venv_path):
        """Create a shortcut/launcher script."""
        python_executable = self.get_python_executable(venv_path)
        
        if os.name == "nt":  # Windows
            # Create batch file
            batch_content = f'''@echo off
cd /d "{self.project_root}"
"{python_executable}" main.py
pause
'''
            batch_file = self.project_root / "run_banking_app.bat"
            with open(batch_file, "w") as f:
                f.write(batch_content)
            logger.info("Created Windows batch file: run_banking_app.bat")
            
        else:  # Unix/Linux/macOS
            # Create shell script
            shell_content = f'''#!/bin/bash
cd "{self.project_root}"
"{python_executable}" main.py
'''
            shell_file = self.project_root / "run_banking_app.sh"
            with open(shell_file, "w") as f:
                f.write(shell_content)
            
            # Make executable
            os.chmod(shell_file, 0o755)
            logger.info("Created Unix shell script: run_banking_app.sh")
    
    def run_tests(self, venv_path):
        """Run basic tests to ensure everything works."""
        python_executable = self.get_python_executable(venv_path)
        
        logger.info("Running basic tests...")
        try:
            # Test if the app can be imported
            result = subprocess.run([
                str(python_executable), "-c", 
                "import main; print('Import test passed')"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Basic tests passed")
            else:
                logger.warning("Some tests failed, but deployment continues")
                
        except Exception as e:
            logger.warning(f"Test execution failed: {e}")
    
    def deploy(self):
        """Run the complete deployment process."""
        logger.info("Starting deployment process...")
        
        # Check Python version
        self.check_python_version()
        
        # Create virtual environment
        venv_path = self.create_virtual_environment()
        
        # Install dependencies
        self.install_dependencies(venv_path)
        
        # Create directories
        self.create_directories()
        
        # Create config file
        self.create_config_file()
        
        # Create shortcut
        self.create_shortcut(venv_path)
        
        # Run tests
        self.run_tests(venv_path)
        
        logger.info("Deployment completed successfully!")
        logger.info(f"Virtual environment: {venv_path}")
        logger.info("To run the application:")
        
        if os.name == "nt":
            logger.info("  Double-click 'run_banking_app.bat' or run:")
            logger.info(f"  {venv_path}\\Scripts\\python.exe main.py")
        else:
            logger.info("  Run './run_banking_app.sh' or:")
            logger.info(f"  {venv_path}/bin/python main.py")

def main():
    """Main deployment function."""
    deployer = Deployer()
    deployer.deploy()

if __name__ == "__main__":
    main() 