# Architecture Decision Records (ADR)

## ADR-001: Use Phi-3 Mini for Language Model
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need to select an appropriate language model for consciousness simulation that can run locally on MacBook Air M1/M2 with 8-16GB RAM while providing sufficient reasoning capabilities.

### Decision
Selected microsoft/Phi-3-mini-4k-instruct (2.7B parameters)

### Rationale
- **Size**: 2.7B parameters fit comfortably in 8GB+ RAM systems
- **Performance**: Excellent reasoning capabilities for size
- **Context**: 4K token window sufficient for consciousness loop context
- **Optimization**: Native support for Apple Silicon via PyTorch MPS
- **Quality**: Strong instruction following and coherent text generation
- **Local**: Can run entirely offline for privacy and reliability

### Consequences
- Enables local execution on consumer hardware
- Provides good reasoning within resource constraints
- May miss some nuanced responses larger models would catch
- Context window limits long-term memory without compression

### Alternatives Considered
- **Llama 3.1 8B**: Too large for consistent MacBook Air performance
- **Gemma 7B**: Better quality but memory constraints
- **Qwen 2.5 3B**: Good performance but less focused on reasoning tasks
- **GPT-4 Mini API**: Would require internet, costs, and privacy concerns

---

## ADR-002: Single-Threaded Consciousness Loop
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need to decide on the concurrency model for the consciousness loop execution - single-threaded sequential or multi-threaded parallel processing.

### Decision
Implement single-threaded sequential consciousness loop

### Rationale
- **Predictability**: Deterministic execution order aids in debugging
- **Simplicity**: Easier to reason about state and side effects  
- **Consciousness Model**: Mimics human consciousness which appears sequential
- **Resource Management**: Avoids race conditions and memory conflicts
- **Apple Silicon**: MPS acceleration handles parallelism within model inference
- **MVP Focus**: Reduces complexity for initial implementation

### Consequences
- Clear, predictable behavior patterns
- Easier debugging and state inspection
- Potentially slower than parallel sensor collection
- May miss some simultaneous environmental events

### Alternatives Considered
- **Multi-threaded**: Parallel sensor collection with synchronized thinking
- **Async/Await**: Non-blocking I/O for sensor reading
- **Process-based**: Separate processes for sensors and thinking

---

## ADR-003: JSON Structured Logging for Analysis
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need logging format that supports both real-time monitoring and post-experiment analysis of consciousness emergence patterns.

### Decision
Use structured JSON logging with comprehensive metadata

### Rationale
- **Analysis Ready**: JSON easily parsed by analysis tools
- **Structured Data**: Consistent format enables pattern recognition
- **Metadata Rich**: Can capture sensor data, timings, emergence indicators
- **Searchable**: Easy to query for specific patterns or timeframes
- **Extensible**: Can add new fields without breaking existing analysis
- **Standards**: JSON is universal format for data exchange

### Consequences
- Enables sophisticated post-experiment analysis
- Larger log files than simple text logging
- Slightly more complex logging code
- Rich data for consciousness emergence research

### Alternatives Considered
- **Plain Text**: Simple but hard to analyze programmatically
- **CSV**: Structured but limited field types and nested data
- **Binary Format**: Compact but requires special tools to read
- **Database**: More complex setup, overkill for MVP

---

## ADR-004: Rich Terminal Interface for MVP
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need user interface that provides real-time consciousness monitoring while keeping implementation simple for MVP.

### Decision
Use Rich library for enhanced terminal-based interface

### Rationale
- **MVP Appropriate**: No GUI complexity, works in terminal
- **Real-time**: Live updates show consciousness state changes
- **Beautiful**: Rich formatting makes monitoring engaging
- **Lightweight**: Minimal resource overhead compared to GUI
- **Cross-platform**: Works on macOS, Linux, Windows
- **Developer Friendly**: Easy to implement and debug

### Consequences
- Professional-looking interface without GUI complexity
- Real-time monitoring capabilities
- Limited to text-based visualizations
- Terminal-only limits some users' preferences

### Alternatives Considered
- **Web Interface**: More complex setup, requires server
- **Native GUI**: Much more complex development
- **Plain Terminal**: Functional but less engaging
- **No Interface**: Pure logging only, harder to monitor

---

## ADR-005: 5% Spontaneous Communication Probability
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need to determine frequency of spontaneous AI communication to balance consciousness simulation with practical observation.

### Decision
5% probability per thinking cycle for spontaneous output

### Rationale
- **Observable**: Frequent enough to see patterns emerge
- **Realistic**: Matches natural communication patterns (most thoughts internal)
- **Controllable**: Prevents overwhelming output flood
- **Adjustable**: Can be tuned based on experimental needs
- **Emergence**: Allows for natural communication timing patterns
- **Research**: Enables study of decision-making patterns

### Consequences
- Regular but not overwhelming spontaneous outputs
- Enables study of communication decision patterns
- Most thoughts remain internal (like human consciousness)
- May miss some interesting thoughts that don't get expressed

### Alternatives Considered
- **1%**: Too rare for meaningful observation
- **10%**: Too frequent, overwhelming output
- **Fixed Timing**: Less realistic than probabilistic approach
- **Always Output**: Would flood interface, not consciousness-like

---

## ADR-006: Apple MPS Acceleration
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need hardware acceleration strategy for optimal performance on Apple Silicon MacBook Air.

### Decision
Use PyTorch MPS (Metal Performance Shaders) backend for GPU acceleration

### Rationale
- **Native**: Built specifically for Apple Silicon architecture
- **Performance**: Significant speedup over CPU-only inference
- **Efficiency**: Better power consumption than CPU-heavy processing
- **Integration**: Seamless PyTorch integration
- **Thermal**: More efficient heat distribution than pure CPU
- **Future-proof**: Apple's recommended acceleration path

### Consequences
- Faster inference times (~2-3x speedup expected)
- Better battery life during long experiments
- Requires macOS and Apple Silicon hardware
- Dependency on Apple's MPS implementation

### Alternatives Considered
- **CPU Only**: Slower, more battery drain, higher heat
- **CUDA**: Not available on Apple Silicon
- **OpenCL**: Deprecated by Apple in favor of Metal
- **Custom Metal**: Too complex for MVP implementation

---

## ADR-007: psutil + sounddevice for Sensors
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need reliable sensor libraries for system metrics and audio level detection across different platforms.

### Decision
Use psutil for system metrics and sounddevice for audio levels

### Rationale
- **Comprehensive**: psutil covers all major system metrics
- **Cross-platform**: Works on macOS, Linux, Windows
- **Stable**: Mature libraries with good APIs
- **Lightweight**: Minimal overhead for data collection
- **Real-time**: Can poll at appropriate frequencies
- **Well-documented**: Good community support and examples

### Consequences
- Reliable sensor data collection
- Cross-platform compatibility
- Additional dependencies to manage
- Audio requires microphone permissions

### Alternatives Considered
- **Platform-specific APIs**: More complex, less portable
- **subprocess system calls**: Less reliable, harder to parse
- **Web APIs**: Would require internet connectivity
- **Custom implementations**: Too much complexity for MVP

---

## ADR-008: Rolling Context Window Management
**Date**: 2024-12-19  
**Status**: Accepted

### Context
Need context management strategy for 4K token limit while maintaining consciousness continuity.

### Decision
Implement rolling context window with compression of older thoughts

### Rationale
- **Memory Efficient**: Stays within 4K token Phi-3 limit
- **Continuity**: Maintains recent consciousness state
- **Scalable**: Can run indefinitely without memory growth
- **Relevant**: Keeps most recent and relevant context
- **Simple**: Straightforward implementation for MVP

### Consequences
- Consciousness maintains short-term coherence
- Long-term memory requires compression/summarization
- Some historical context may be lost
- Predictable memory usage patterns

### Alternatives Considered
- **Fixed Context**: Would eventually overflow
- **External Memory**: More complex implementation
- **Summarization**: Would require additional AI processing
- **No Context Management**: Would cause failures at token limit 