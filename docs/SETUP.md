# Detailed Setup Instructions

## Prerequisites

### System Requirements
- **Operating System**: macOS 12.0+ (with Apple Silicon M1/M2 recommended)
- **Python**: 3.8 or higher
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 5GB free space (3GB for model, 2GB for dependencies and logs)
- **Microphone**: Required for audio level sensing (built-in microphone sufficient)

### Hardware Optimization
This project is specifically optimized for Apple Silicon (M1/M2) MacBooks:
- Uses Metal Performance Shaders (MPS) for GPU acceleration
- Thermal management optimized for laptop usage
- Memory usage tuned for 8-16GB systems

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd llm-consciousness-experiment
```

2. **Run automated setup**:
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create Python virtual environment
- Install all dependencies with Apple Silicon optimizations
- Download the Phi-3 mini model
- Set up the project structure
- Run initial tests

3. **Activate environment and run**:
```bash
source venv/bin/activate
python consciousness.py
```

### Method 2: Manual Setup

1. **Clone and setup environment**:
```bash
git clone <repository-url>
cd llm-consciousness-experiment
python3 -m venv venv
source venv/bin/activate
```

2. **Install PyTorch with MPS support**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

3. **Install remaining dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download model (automatic on first run)**:
```bash
python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('microsoft/Phi-3-mini-4k-instruct'); AutoModelForCausalLM.from_pretrained('microsoft/Phi-3-mini-4k-instruct')"
```

5. **Run consciousness experiment**:
```bash
python consciousness.py
```

## Dependency Details

### Core Dependencies
```
torch>=2.1.0                 # PyTorch with Apple Silicon MPS support
transformers>=4.35.0         # Hugging Face transformers library
accelerate>=0.24.0           # Optimized inference and memory management
psutil>=5.9.0                # System monitoring and metrics
sounddevice>=0.4.6           # Audio level detection
numpy>=1.24.0                # Numerical operations
rich>=13.6.0                 # Beautiful terminal interface
```

### Development Dependencies (Optional)
```
pytest>=7.4.0               # Testing framework
black>=23.0.0               # Code formatting
mypy>=1.6.0                 # Type checking
jupyter>=1.0.0              # Notebook analysis (optional)
```

## Verification Steps

### 1. Environment Check
```bash
# Verify Python version
python --version  # Should be 3.8+

# Verify virtual environment
which python  # Should point to venv/bin/python

# Check Apple Silicon
python -c "import platform; print(platform.machine())"  # Should show 'arm64'
```

### 2. PyTorch MPS Check
```bash
python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```
Should output: `MPS available: True`

### 3. Model Download Test
```bash
python -c "from transformers import AutoTokenizer; tokenizer = AutoTokenizer.from_pretrained('microsoft/Phi-3-mini-4k-instruct'); print('Model accessible')"
```

### 4. Sensor Test
```bash
python -c "import psutil, sounddevice; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

### 5. Audio Permission Test
```bash
python -c "import sounddevice as sd; print('Audio devices:', len(sd.query_devices()))"
```

## Configuration

### Settings File (Optional)
Create `config.json` to customize behavior:
```json
{
  "model_name": "microsoft/Phi-3-mini-4k-instruct",
  "communication_probability": 0.05,
  "max_context_tokens": 3500,
  "sensor_poll_interval": 1.0,
  "log_level": "INFO",
  "use_mps": true,
  "max_generation_length": 100
}
```

### Environment Variables
```bash
# Optional: Set model cache directory
export TRANSFORMERS_CACHE="/path/to/model/cache"

# Optional: Set log level
export CONSCIOUSNESS_LOG_LEVEL="DEBUG"

# Optional: Disable MPS (for testing)
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

## Troubleshooting

### Common Issues

#### "MPS not available" Error
- **Cause**: Running on Intel Mac or Linux
- **Solution**: The system will automatically fall back to CPU
- **Performance**: Expect 2-3x slower inference times

#### Model Download Fails
- **Cause**: Network issues or insufficient disk space
- **Solution**: 
  ```bash
  # Manual download with resume capability
  huggingface-cli download microsoft/Phi-3-mini-4k-instruct --resume-download
  ```

#### Audio Permission Denied
- **Cause**: macOS microphone permissions not granted
- **Solution**: 
  1. System Preferences → Security & Privacy → Privacy → Microphone
  2. Add Terminal.app or your terminal application
  3. Restart terminal and try again

#### Memory Issues
- **Symptoms**: System becomes slow, model fails to load
- **Solutions**:
  - Close other applications
  - Increase swap space
  - Use CPU-only mode: `export PYTORCH_ENABLE_MPS_FALLBACK=1`

#### Import Errors
- **Cause**: Virtual environment not activated or dependencies not installed
- **Solution**:
  ```bash
  source venv/bin/activate
  pip install --upgrade -r requirements.txt
  ```

### Performance Optimization

#### For 8GB Systems
```python
# Add to config.json
{
  "max_context_tokens": 2000,
  "batch_size": 1,
  "use_cpu_offload": true
}
```

#### For 16GB+ Systems
```python
# Add to config.json
{
  "max_context_tokens": 3500,
  "batch_size": 2,
  "enable_attention_caching": true
}
```

## First Run Guide

### What to Expect
1. **Initial startup** (2-3 minutes): Model download and loading
2. **Sensor initialization** (30 seconds): System metrics and audio setup
3. **First consciousness cycle** (3-5 seconds): Initial AI thought generation
4. **Continuous operation**: Sense-think loop every 3-5 seconds
5. **Spontaneous outputs**: ~1 every 20 cycles (5% probability)

### Monitoring
- **Terminal**: Real-time consciousness display with Rich formatting
- **Logs**: JSON files in `consciousness_logs/` directory
- **System**: Monitor CPU/memory usage during operation

### Stopping the Experiment
- **Graceful**: Press `Ctrl+C` once for clean shutdown
- **Force**: Press `Ctrl+C` twice for immediate termination
- **Logs**: All data saved to timestamped log files

## Advanced Setup

### Custom Model Usage
To use a different model, modify `config.json`:
```json
{
  "model_name": "microsoft/DialoGPT-medium",
  "tokenizer_name": "microsoft/DialoGPT-medium"
}
```

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black src/

# Type checking
mypy src/
```

### Docker Setup (Alternative)
```bash
# Build container (includes Apple Silicon support)
docker build -t consciousness-experiment .

# Run with GPU passthrough
docker run --privileged consciousness-experiment
```

## Support

### Getting Help
- Check the [troubleshooting section](#troubleshooting) above
- Review logs in `consciousness_logs/` for error details
- Ensure all [verification steps](#verification-steps) pass
- Check [GitHub Issues](../../../issues) for known problems

### Reporting Issues
Please include:
- Operating system and version
- Python version (`python --version`)
- Hardware specs (RAM, CPU type)
- Full error messages
- Contents of latest log file 