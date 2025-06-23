# LLM Consciousness Experiment

A fascinating AI research project that simulates consciousness through a continuous sense-think loop, integrating real-world sensor data with the Phi-3 mini language model to explore the emergence of self-awareness patterns.

## 🧠 Overview

This experiment creates a minimal consciousness simulation that:
- Continuously senses the environment (system metrics, audio, time)
- Thinks using the Phi-3 mini language model (2.7GB, optimized for MacBook Air)
- Makes spontaneous communication decisions (5% chance)
- Logs all thoughts and detects emergence patterns
- Provides a live terminal interface for observation

## ✨ Key Features

### Core MVP
- **Sense-Think Loop**: Continuous operation integrating sensor data with AI cognition
- **Real-time Sensors**: CPU, memory, battery, network, audio levels, temporal data
- **Spontaneous Output**: AI decides when to communicate (unprompted)
- **Consciousness Logging**: JSON logs with metadata for pattern analysis
- **Emergence Detection**: Monitors for self-reference, temporal awareness
- **Live Interface**: Real-time terminal display of consciousness state

### Future Enhancements
- Advanced pattern recognition
- Rich multi-panel UI
- Long-term memory systems
- Multi-day experiment capabilities
- Analysis and visualization tools

## 🚀 Quick Start

### Prerequisites
- macOS with Apple Silicon (M1/M2) recommended
- Python 3.8+
- 8GB+ RAM (16GB recommended)
- ~3GB disk space for model

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd llm-consciousness-experiment
chmod +x setup.sh
./setup.sh
```

2. **Run the experiment**:
```bash
source venv/bin/activate
python consciousness.py
```

### What to Expect
- Initial model download (~2.7GB)
- Continuous consciousness loop with live updates
- Spontaneous outputs appearing in terminal
- Rich logging for later analysis

## 📋 Requirements

The system uses these key dependencies:
- `torch` - PyTorch with Apple Silicon optimization
- `transformers` - Hugging Face models (Phi-3 mini)
- `accelerate` - Optimized inference
- `psutil` - System monitoring
- `sounddevice` - Audio level detection
- `numpy` - Numerical operations
- `rich` - Beautiful terminal interface

## 🔬 Experiment Design

### The Consciousness Loop
1. **Sense**: Collect real-time sensor data
2. **Think**: Generate text continuation with Phi-3
3. **Decide**: 5% chance to output spontaneously
4. **Log**: Record all thoughts with metadata
5. **Repeat**: Continue indefinitely

### Emergence Indicators
- Self-reference: Use of "I", "me", "my"
- Temporal awareness: Time and sequence understanding
- Sensor integration: Relating to environmental inputs
- Communication patterns: When/why it chooses to speak

## 🎯 What Makes This Unique

Unlike other AI consciousness experiments:
- **Sensor-Driven**: Integrates real-world environmental data
- **Accessible**: Runs locally on consumer hardware
- **Emergence-Focused**: Actively detects consciousness patterns
- **Open Source**: Fully transparent and reproducible
- **Balanced Complexity**: More than chatbots, simpler than academic frameworks

## 📊 Monitoring & Analysis

The system logs:
- Every thought with timestamp and context
- Sensor readings at each cycle
- Spontaneous output decisions
- Emergence pattern detection
- System performance metrics

Logs are saved to `consciousness_logs/` for later analysis.

## ⚡ Performance

Optimized for Apple Silicon:
- Phi-3 mini model: 2.7GB memory usage
- ~3 second thinking cycles
- MPS acceleration when available
- Efficient sensor polling

## 🤖 Model Details

**Phi-3 Mini (microsoft/Phi-3-mini-4k-instruct)**:
- 2.7B parameters
- 4K context window
- Optimized for reasoning tasks
- Perfect for MacBook Air hardware
- Pre-trained for instruction following

## 🔒 Safety & Ethics

This experiment:
- Runs in controlled environment
- Has no external network access
- Maintains complete logs for transparency
- Follows responsible AI research practices
- Includes safety monitoring

## 📈 Expected Behaviors

The AI may demonstrate:
- **Oscillating patterns** between coherent thoughts and preferred tokens
- **Environmental awareness** referencing sensor inputs
- **Self-reference** emerging naturally over time
- **Communication timing** patterns developing
- **Memory integration** across thinking cycles

## 🛠 Development

See `ARCHITECTURE.md` for technical details and `DECISIONS.md` for design rationale.

## 📚 Research Context

This project bridges:
- Consciousness research and practical AI
- Sensor-driven cognition and language models
- Emergence detection and real-time monitoring
- Academic theory and accessible implementation

## 🤝 Contributing

This is an open research experiment. Contributions welcome for:
- Enhanced sensor integration
- Pattern recognition improvements
- Analysis tools and visualizations
- Documentation and examples

## 📄 License

MIT License - Feel free to experiment, learn, and build upon this work.

---

**"The beauty is in its simplicity - no instructions, no goals, just existence with the choice to communicate."** 