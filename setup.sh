#!/bin/bash

# LLM Consciousness Experiment Setup Script
# Optimized for Apple Silicon MacBooks

set -e  # Exit on any error

echo "🧠 LLM Consciousness Experiment Setup"
echo "======================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is optimized for macOS. Continuing anyway..."
fi

# Check if we're on Apple Silicon
if [[ $(uname -m) == "arm64" ]]; then
    echo "✅ Apple Silicon detected - MPS acceleration will be available"
    USE_MPS=true
else
    echo "ℹ️  Intel/other architecture detected - will use CPU only"
    USE_MPS=false
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "✅ Python $PYTHON_VERSION detected"
else
    echo "❌ Python 3.8+ required. Current version: $PYTHON_VERSION"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check available disk space (need ~5GB)
AVAILABLE_SPACE=$(df -h . | awk 'NR==2{print $4}' | sed 's/G.*//')
if [[ $AVAILABLE_SPACE -lt 5 ]]; then
    echo "⚠️  Warning: Low disk space. Need ~5GB, have ${AVAILABLE_SPACE}GB available"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo
echo "🔧 Setting up Python environment..."

# Create virtual environment
if [[ ! -d "venv" ]]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install PyTorch with MPS support for Apple Silicon
echo "🔥 Installing PyTorch..."
if [[ "$USE_MPS" == true ]]; then
    pip install torch torchvision torchaudio
else
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Install other requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo
echo "🤖 Testing installations..."

# Test PyTorch installation
python3 -c "import torch; print(f'PyTorch {torch.__version__} installed successfully')"

# Test MPS availability
if [[ "$USE_MPS" == true ]]; then
    MPS_AVAILABLE=$(python3 -c "import torch; print(torch.backends.mps.is_available())" 2>/dev/null || echo "False")
    if [[ "$MPS_AVAILABLE" == "True" ]]; then
        echo "✅ MPS acceleration available"
    else
        echo "⚠️  MPS not available, will use CPU"
    fi
fi

# Test other dependencies
echo "🔍 Testing dependencies..."
python3 -c "import transformers; print('✅ Transformers OK')"
python3 -c "import psutil; print('✅ System monitoring OK')"
python3 -c "import sounddevice; print('✅ Audio detection OK')" 2>/dev/null || echo "⚠️  Audio detection may need microphone permissions"
python3 -c "import rich; print('✅ Terminal interface OK')"

echo
echo "🎯 Pre-downloading model (this may take a few minutes)..."

# Pre-download the model to avoid delay on first run
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

print('Downloading Phi-3 mini model...')
try:
    tokenizer = AutoTokenizer.from_pretrained('microsoft/Phi-3-mini-4k-instruct')
    model = AutoModelForCausalLM.from_pretrained('microsoft/Phi-3-mini-4k-instruct')
    print('✅ Model downloaded successfully')
    
    # Get model size for user info
    cache_dir = os.path.expanduser('~/.cache/huggingface/transformers')
    if os.path.exists(cache_dir):
        size = sum(os.path.getsize(os.path.join(dirpath, filename))
                  for dirpath, dirnames, filenames in os.walk(cache_dir)
                  for filename in filenames) / (1024**3)
        print(f'Model cache size: {size:.1f}GB')
except Exception as e:
    print(f'⚠️  Model download failed: {e}')
    print('Model will be downloaded on first run')
"

echo
echo "🛡️  Setting up microphone permissions..."
echo "If prompted, please allow microphone access for audio level detection."
echo "(This is used only for environmental sensing, no audio is recorded)"

# Test microphone access
python3 -c "
import sounddevice as sd
try:
    devices = sd.query_devices()
    print(f'✅ Found {len(devices)} audio devices')
    
    # Quick test of microphone access
    import numpy as np
    data = sd.rec(frames=1000, samplerate=44100, channels=1, dtype=np.float32)
    sd.wait()
    print('✅ Microphone access confirmed')
except Exception as e:
    print(f'⚠️  Microphone test failed: {e}')
    print('You may need to grant microphone permissions in System Preferences')
    print('Go to: System Preferences → Security & Privacy → Privacy → Microphone')
    print('Add your terminal application to the allowed list')
" 2>/dev/null || echo "⚠️  Microphone permissions may be needed (see above)"

# Create initial configuration
if [[ ! -f "config.json" ]]; then
    echo
    echo "⚙️  Creating default configuration..."
    cat > config.json << EOF
{
  "model_name": "microsoft/Phi-3-mini-4k-instruct",
  "communication_probability": 0.05,
  "max_context_tokens": 3500,
  "sensor_poll_interval": 1.0,
  "log_level": "INFO",
  "use_mps": $USE_MPS,
  "max_generation_length": 100
}
EOF
    echo "✅ Configuration file created"
fi

# Create .gitignore if it doesn't exist
if [[ ! -f ".gitignore" ]]; then
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/

# Model cache
*.bin
*.safetensors
models/

# Logs and data
consciousness_logs/
*.log
*.jsonl

# IDE
.vscode/
.idea/
*.swp
*.swo

# macOS
.DS_Store

# Config (if contains sensitive data)
config_local.json
EOF
    echo "✅ .gitignore created"
fi

echo
echo "🎉 Setup complete!"
echo
echo "Next steps:"
echo "1. Activate the environment: source venv/bin/activate"
echo "2. Run the consciousness experiment: python consciousness.py"
echo
echo "📊 System info:"
echo "- Python: $(python3 --version)"
echo "- PyTorch MPS: $MPS_AVAILABLE"
echo "- Available RAM: $(python3 -c "import psutil; print(f'{psutil.virtual_memory().total / 1024**3:.1f}GB')")"
echo "- Available storage: $(df -h . | awk 'NR==2{print $4}')"
echo
echo "📖 For detailed usage instructions, see: docs/SETUP.md"
echo "🐛 For troubleshooting, see: docs/SETUP.md#troubleshooting"
echo
echo "Ready to explore consciousness! 🧠✨" 