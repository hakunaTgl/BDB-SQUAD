#!/usr/bin/env python3
"""
AetherOS Creative Studio Launcher
Smart launcher that handles dependencies and environment setup
"""

import sys
import subprocess
import os
from pathlib import Path


class AetherOSLauncher:
    """Intelligent launcher for AetherOS Creative Studio"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_minimal = ["gradio>=4.0.0"]
        self.requirements_full = self.project_root / "requirements.txt"
        
    def print_banner(self):
        """Print startup banner"""
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🎨 AetherOS Creative Studio 🎨                         ║
║                                                                              ║
║              The Open-Source AI Storytelling Engine                          ║
║                  Democratizing imagination since 2024                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)
    
    def check_dependency(self, package_name: str) -> bool:
        """Check if a package is installed"""
        try:
            __import__(package_name.replace("-", "_"))
            return True
        except ImportError:
            return False
    
    def check_environment(self) -> dict:
        """Check the current environment and dependencies"""
        print("🔍 Checking environment...")
        
        status = {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "gradio_available": self.check_dependency("gradio"),
            "minimal_mode": True,
            "disk_space_warning": False
        }
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("⚠️  Warning: Python 3.8+ recommended")
        else:
            print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        # Check Gradio
        if status["gradio_available"]:
            print("✅ Gradio (Web Interface)")
            status["minimal_mode"] = False
        else:
            print("⚠️  Gradio not found (terminal interface will be used)")
        
        # Check optional dependencies
        optional_deps = {
            "numpy": "NumPy",
            "networkx": "NetworkX",
            "torch": "PyTorch",
            "transformers": "Transformers"
        }
        
        for pkg, name in optional_deps.items():
            if self.check_dependency(pkg):
                print(f"✅ {name}")
            else:
                print(f"ℹ️  {name} (optional, not installed)")
        
        # Check disk space
        try:
            stat = os.statvfs(self.project_root)
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if free_gb < 1:
                status["disk_space_warning"] = True
                print(f"⚠️  Low disk space: {free_gb:.2f} GB free")
            else:
                print(f"✅ Disk space: {free_gb:.2f} GB free")
        except:
            pass
        
        return status
    
    def offer_installation(self, status: dict) -> bool:
        """Offer to install missing dependencies"""
        
        if status["minimal_mode"] and not status["gradio_available"]:
            print("\n" + "="*80)
            print("📦 DEPENDENCY INSTALLATION")
            print("="*80)
            print()
            print("For the full web interface experience, we recommend installing Gradio.")
            print()
            print("Options:")
            print("  1. Install Gradio only (minimal, ~50 MB)")
            print("  2. Install all dependencies (full features, ~5 GB)")
            print("  3. Continue with terminal interface (no installation)")
            print("  4. Exit")
            print()
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                return self.install_minimal()
            elif choice == "2":
                if status["disk_space_warning"]:
                    print("\n⚠️  Warning: You may not have enough disk space!")
                    confirm = input("Continue anyway? (y/n): ").lower()
                    if confirm != 'y':
                        return False
                return self.install_full()
            elif choice == "3":
                return True
            else:
                return False
        
        return True
    
    def install_minimal(self) -> bool:
        """Install minimal dependencies (Gradio only)"""
        print("\n⏳ Installing Gradio...")
        print("This will take 1-2 minutes and requires ~50 MB of disk space.")
        print()
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--upgrade", "pip", "--quiet"
            ])
            
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "gradio>=4.0.0", "--quiet"
            ])
            
            print("✅ Gradio installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            print()
            print("You can try manually with:")
            print("  pip install gradio")
            return False
    
    def install_full(self) -> bool:
        """Install full dependencies"""
        print("\n⏳ Installing full dependencies...")
        print("This may take 10-15 minutes and requires ~5 GB of disk space.")
        print()
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--upgrade", "pip", "--quiet"
            ])
            
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "-r", str(self.requirements_full), "--quiet"
            ])
            
            print("✅ All dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            print()
            print("You can try manually with:")
            print(f"  pip install -r {self.requirements_full}")
            return False
    
    def launch_interface(self, mode: str = "auto"):
        """Launch the appropriate interface"""
        
        print("\n" + "="*80)
        print("🚀 LAUNCHING AETHEROS STUDIO")
        print("="*80)
        print()
        
        # Determine which interface to launch
        if mode == "auto":
            if self.check_dependency("gradio"):
                mode = "web"
            else:
                mode = "terminal"
        
        if mode == "web":
            print("🌐 Launching web interface...")
            print()
            print("The interface will open in your browser at:")
            print("  http://localhost:7860")
            print()
            print("Press Ctrl+C to stop the server")
            print()
            
            try:
                subprocess.run([sys.executable, "aetheros_interface.py"])
            except KeyboardInterrupt:
                print("\n\n👋 Shutting down...")
            
        else:
            print("💻 Launching terminal interface...")
            print()
            subprocess.run([sys.executable, "aetheros_interface.py"])
    
    def show_help(self):
        """Show help information"""
        print("""
AETHEROS CREATIVE STUDIO - QUICK START GUIDE

🎨 WHAT IS AETHEROS?
  A fully open-source AI-powered creative studio for multimodal storytelling.
  No coding required—just your imagination!

🚀 QUICK START

  1. SIMPLE MODE (No Installation)
     Just run: python launch_studio.py
     Uses terminal interface with zero dependencies.

  2. WEB INTERFACE (Recommended)
     Install Gradio: pip install gradio
     Then run: python launch_studio.py
     Beautiful web interface at http://localhost:7860

  3. FULL FEATURES (Advanced)
     Install all dependencies: pip install -r requirements.txt
     Enables all AI capabilities and advanced features.

📚 USAGE

  Terminal Interface:
    - Follow on-screen prompts
    - Enter your story ideas
    - View generated content

  Web Interface:
    - Open browser to http://localhost:7860
    - Fill in the story prompt form
    - Click "Generate Content"
    - View results in real-time

🎯 EXAMPLES

  Try these prompts:
    • "A wizard discovers a book that can rewrite reality"
    • "A detective gets an anonymous letter about a cold case"
    • "An astronaut finds strange signals on Mars"

💡 TIPS

  - Start with simple prompts to test the system
  - Mix emotional tones for complex narratives
  - View history to see all your creations
  - Check statistics to see system performance

📖 LEARN MORE

  - README.md - Full documentation
  - QUICKSTART.md - Detailed guide
  - STATUS.md - Current capabilities

🐛 TROUBLESHOOTING

  - "Gradio not found" - Install with: pip install gradio
  - "Disk space error" - Free up space or use terminal mode
  - "Import errors" - Use terminal mode (zero dependencies)

═══════════════════════════════════════════════════════════════════════════════
        """)
    
    def run(self):
        """Main launcher flow"""
        self.print_banner()
        
        # Check for help flag
        if "--help" in sys.argv or "-h" in sys.argv:
            self.show_help()
            return
        
        # Check environment
        status = self.check_environment()
        
        print()
        
        # Offer installation if needed
        if not self.offer_installation(status):
            print("\n👋 Exiting. Run again anytime!")
            return
        
        # Launch interface
        self.launch_interface()


if __name__ == "__main__":
    launcher = AetherOSLauncher()
    launcher.run()
