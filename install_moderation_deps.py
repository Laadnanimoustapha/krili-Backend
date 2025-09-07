"""
Installation script for Chat Moderation System dependencies
"""
import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🛡️ Installing Chat Moderation System Dependencies")
    print("=" * 50)
    
    # Core dependencies (required)
    core_packages = [
        "numpy",
        "pandas", 
        "scikit-learn",
        "flask",
        "flask-cors"
    ]
    
    # Optional dependencies (enhance functionality)
    optional_packages = [
        "phonenumbers",
        "langdetect",
        "streamlit",
        "plotly",
        "psutil"
    ]
    
    print("\n📦 Installing core packages...")
    core_success = 0
    for package in core_packages:
        if install_package(package):
            core_success += 1
    
    print(f"\n✅ Core packages: {core_success}/{len(core_packages)} installed successfully")
    
    print("\n🔧 Installing optional packages...")
    optional_success = 0
    for package in optional_packages:
        if install_package(package):
            optional_success += 1
    
    print(f"\n✅ Optional packages: {optional_success}/{len(optional_packages)} installed successfully")
    
    print("\n🎯 Installation Summary:")
    print(f"   Core packages: {core_success}/{len(core_packages)}")
    print(f"   Optional packages: {optional_success}/{len(optional_packages)}")
    
    if core_success == len(core_packages):
        print("\n🎉 Installation complete! You can now run:")
        print("   python chat_moderation_system.py example")
        print("   python chat_moderation_system.py api")
    else:
        print("\n⚠️ Some core packages failed to install.")
        print("   The system may have limited functionality.")
    
    print("\n📚 Next steps:")
    print("1. Run examples: python chat_moderation_system.py example")
    print("2. Start API server: python chat_moderation_system.py api")
    print("3. Train models: python chat_moderation_system.py train")

if __name__ == "__main__":
    main()