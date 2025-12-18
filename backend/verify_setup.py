"""
Setup Verification Script
Run this to verify your backend is configured correctly
"""
import os
import sys
from config import settings


def check_environment():
    """Check if environment variables are set correctly"""
    print("🔍 Checking environment configuration...")
    print(f"   LLM Provider: {settings.LLM_PROVIDER}")
    print(f"   Embedding Provider: {settings.EMBEDDING_PROVIDER}")
    print(f"   Vector DB Type: {settings.VECTOR_DB_TYPE}")
    
    # Check API keys
    if settings.LLM_PROVIDER.lower() == "openai":
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            print("   ⚠️  WARNING: OPENAI_API_KEY not set or using placeholder")
        else:
            print("   ✅ OPENAI_API_KEY is set")
    
    if settings.LLM_PROVIDER.lower() == "gemini":
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_api_key_here":
            print("   ⚠️  WARNING: GEMINI_API_KEY not set or using placeholder")
        else:
            print("   ✅ GEMINI_API_KEY is set")
    
    print()


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking Python dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain",
        "youtube_transcript_api",
        "pydantic"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n   ⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("\n   ✅ All required packages installed")
    
    print()


def check_directories():
    """Check if required directories exist"""
    print("📁 Checking directories...")
    
    dirs = [
        settings.CACHE_DIR,
        settings.VECTOR_DB_PATH
    ]
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ⚠️  {dir_path} - will be created automatically")
    
    print()


def main():
    """Run all checks"""
    print("=" * 50)
    print("YouTube Chatbot - Setup Verification")
    print("=" * 50)
    print()
    
    check_environment()
    check_dependencies()
    check_directories()
    
    print("=" * 50)
    print("✅ Verification complete!")
    print()
    print("Next steps:")
    print("1. Make sure your .env file is configured")
    print("2. Run: python main.py")
    print("3. Test: curl http://localhost:8000/health")
    print("=" * 50)


if __name__ == "__main__":
    main()

