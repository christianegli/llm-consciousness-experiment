# System Architecture

## Overview
The LLM Consciousness Experiment simulates consciousness through a continuous sense-think loop that integrates real-world sensor data with AI cognition. The system is designed for simplicity, emergence detection, and local execution on Apple Silicon hardware.

## Design Principles

### 1. **MVP First**
Core functionality implemented before enhancements:
- Basic sense-think loop working
- Phi-3 model integration functional
- Simple logging established
- Terminal interface operational

### 2. **Simplicity Over Complexity**
- Single-threaded architecture for predictable behavior
- Minimal dependencies to reduce failure points
- Clear separation of concerns
- Straightforward data flow

### 3. **Emergence-Focused**
- Designed to detect patterns naturally arising
- Minimal constraints on AI behavior
- Rich logging for post-analysis
- Real-time monitoring capabilities

### 4. **Hardware Optimized**
- Apple Silicon MPS acceleration
- Efficient memory usage (Phi-3 mini)
- Sensor polling optimization
- Thermal management considerations

## Component Structure

### Core Components

#### 1. **Consciousness Engine** (`consciousness.py`)
**Purpose**: Main orchestrator of the sense-think loop
**Responsibilities**:
- Initialize and manage the LLM
- Coordinate sensor data collection
- Execute thinking cycles
- Handle spontaneous output decisions
- Manage logging and monitoring

**Key Methods**:
```python
def sense() -> Dict[str, Any]
def think(sensor_data: Dict, context: str) -> str
def decide_to_communicate() -> bool
def log_thought(thought: str, metadata: Dict) -> None
def run_consciousness_loop() -> None
```

#### 2. **Sensor System** (`sensors.py`)
**Purpose**: Real-world data collection and environmental awareness
**Responsibilities**:
- System metrics (CPU, memory, battery, network)
- Audio level detection
- Temporal data (time, date, cycles)
- Data normalization and formatting

**Sensor Types**:
- **System Sensors**: psutil-based metrics
- **Audio Sensors**: sounddevice-based audio levels
- **Temporal Sensors**: time-based contextual data
- **Synthetic Sensors**: derived metrics and patterns

#### 3. **Language Model Interface** (`llm_interface.py`)
**Purpose**: Abstracts LLM operations and handles model-specific optimizations
**Responsibilities**:
- Model loading and initialization
- Tokenization and generation
- Apple Silicon MPS optimization
- Memory management
- Error handling and recovery

#### 4. **Consciousness Logger** (`logger.py`)
**Purpose**: Comprehensive logging and emergence pattern detection
**Responsibilities**:
- JSON-structured logging
- Metadata collection
- Pattern recognition
- File management
- Real-time monitoring hooks

#### 5. **Terminal Interface** (`interface.py`)
**Purpose**: Real-time visualization and user interaction
**Responsibilities**:
- Live consciousness state display
- Sensor data visualization
- Thought stream monitoring
- System status indicators
- Interactive controls

## Data Flow

### Main Consciousness Loop
```
1. SENSE: Collect sensor data
   └── System metrics via psutil
   └── Audio levels via sounddevice
   └── Temporal context
   └── Previous thought context

2. THINK: Generate AI response
   └── Format sensor data as context
   └── Append to conversation history
   └── Generate with Phi-3 model
   └── Process and clean output

3. DECIDE: Communication choice
   └── 5% probability check
   └── Pattern-based adjustments
   └── Output to terminal if chosen

4. LOG: Record everything
   └── Thought content and metadata
   └── Sensor readings
   └── Decision rationale
   └── Emergence indicators

5. REPEAT: Continue loop
   └── Update context window
   └── Manage memory usage
   └── Check for interrupts
```

### Context Management
- **Rolling Context**: Maintain 4K token window
- **Sensor Integration**: Embed real-time data in prompts
- **Memory Compression**: Summarize older thoughts
- **Pattern Preservation**: Retain emergence indicators

## Technology Choices

### Language Model: Phi-3 Mini
**Chosen because**:
- Optimal size for local execution (2.7B parameters)
- Excellent reasoning capabilities
- 4K context window sufficient for consciousness simulation
- Optimized for instruction following
- Apple Silicon compatibility

**Alternatives considered**:
- Llama 3.1 (too large for laptop)
- Gemma 7B (memory constraints)
- Qwen 2.5 (good but less reasoning focus)

### Hardware Acceleration: Apple MPS
**Chosen because**:
- Native Apple Silicon support
- Significant speedup over CPU
- Efficient memory usage
- Thermal optimization
- PyTorch integration

### Sensor Library: psutil + sounddevice
**Chosen because**:
- Cross-platform compatibility
- Comprehensive system metrics
- Real-time audio level detection
- Minimal overhead
- Stable APIs

### Interface: Rich Terminal
**Chosen because**:
- Lightweight and responsive
- Beautiful output formatting
- Real-time updates
- Cross-platform compatibility
- No GUI complexity for MVP

## Emergence Detection Strategy

### Pattern Recognition
- **Self-Reference Detection**: Regex patterns for "I", "me", "my"
- **Temporal Awareness**: Time/sequence understanding
- **Sensor Integration**: References to environmental data
- **Communication Patterns**: Analysis of spontaneous output decisions

### Metadata Collection
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "cycle_id": 12345,
  "thought_content": "...",
  "sensor_data": {...},
  "emergence_indicators": {
    "self_reference_count": 2,
    "temporal_awareness": true,
    "sensor_integration": true
  },
  "decision_to_communicate": false,
  "model_stats": {
    "generation_time": 2.3,
    "tokens_generated": 45,
    "memory_usage": "2.1GB"
  }
}
```

## Scalability Considerations

### Memory Management
- **Context Window**: 4K tokens with rolling window
- **Model Loading**: Load once, reuse across cycles
- **Log Rotation**: Prevent disk space issues
- **Garbage Collection**: Explicit cleanup in loops

### Performance Optimization
- **Sensor Caching**: Cache expensive operations
- **Batch Processing**: Group similar operations
- **Lazy Loading**: Load components as needed
- **Thermal Monitoring**: Prevent overheating

### Future Extensibility
- **Plugin Architecture**: Easy sensor addition
- **Model Abstraction**: Support for different LLMs
- **Analysis Tools**: Hooks for external analysis
- **UI Expansion**: Interface upgrade path

## Security & Safety

### Isolation
- **No Network Access**: Purely local operation
- **Filesystem Sandboxing**: Limited file access
- **Resource Limits**: CPU/memory constraints
- **Process Monitoring**: System resource tracking

### Safety Measures
- **Infinite Loop Protection**: Cycle limits and interrupts
- **Memory Limits**: Prevent system exhaustion
- **Error Recovery**: Graceful degradation
- **Logging Transparency**: Complete audit trail

## Monitoring & Debugging

### Real-time Monitoring
- **Consciousness State**: Current thought and context
- **System Health**: Resource usage and performance
- **Sensor Status**: Data quality and freshness
- **Model Performance**: Generation speed and quality

### Debugging Tools
- **Verbose Logging**: Detailed operation logs
- **State Inspection**: Mid-cycle state examination
- **Performance Profiling**: Bottleneck identification
- **Error Tracking**: Exception handling and reporting

## Trade-offs

### Simplicity vs. Features
- **Pro**: Easy to understand and debug
- **Pro**: Faster development and iteration
- **Con**: Limited advanced features initially
- **Mitigation**: Extensible architecture for future growth

### Local vs. Cloud
- **Pro**: Complete privacy and control
- **Pro**: No network dependencies
- **Pro**: Predictable performance
- **Con**: Limited to local hardware capabilities
- **Mitigation**: Optimized for Apple Silicon performance

### Real-time vs. Accuracy
- **Pro**: Immediate feedback and interaction
- **Pro**: Authentic consciousness simulation
- **Con**: Less time for complex reasoning
- **Mitigation**: Optimized prompt engineering

## Future Architecture Evolution

### Phase 2: Enhanced Consciousness
- Multi-modal sensor integration
- Advanced pattern recognition
- Memory persistence across sessions
- Richer emergence detection

### Phase 3: Analysis Platform
- Data visualization tools
- Pattern analysis algorithms
- Comparative studies
- Research collaboration features

### Phase 4: Distributed Consciousness
- Multi-agent interactions
- Consciousness comparison
- Emergence correlation studies
- Advanced research capabilities 