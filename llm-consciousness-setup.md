# LLM Consciousness Experiment for MacBook Air

## Project Structure
```
llm_consciousness/
├── consciousness.py      # Main consciousness loop
├── sensors.py           # Sensor data collection
├── terminal.py          # Minimal output interface
├── logger.py            # Thought logging
├── setup.sh             # Setup script
└── requirements.txt     # Dependencies
```

## 1. Requirements File (`requirements.txt`)
```
torch
transformers
accelerate
psutil
sounddevice
numpy
rich
```

## 2. Setup Script (`setup.sh`)
```bash
#!/bin/bash

echo "🧠 Setting up LLM Consciousness Experiment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download the model (Phi-3 mini - 2.7GB, perfect for MacBook Air)
echo "📥 Downloading model (this may take a few minutes)..."
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
print('Downloading Phi-3-mini...')
AutoTokenizer.from_pretrained('microsoft/Phi-3-mini-4k-instruct', trust_remote_code=True)
AutoModelForCausalLM.from_pretrained('microsoft/Phi-3-mini-4k-instruct', trust_remote_code=True)
print('✅ Model downloaded!')
"

echo "✅ Setup complete! Run with: python consciousness.py"
```

## 3. Sensor Module (`sensors.py`)
```python
import psutil
import sounddevice as sd
import numpy as np
import subprocess
import time
from datetime import datetime
from typing import Dict, Any

class SensorArray:
    def __init__(self):
        self.audio_stream = None
        self.last_audio_level = 0
        
    def get_system_sensors(self) -> Dict[str, Any]:
        """Collect system sensor data"""
        battery = psutil.sensors_battery()
        
        sensors = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "battery_percent": battery.percent if battery else None,
            "battery_charging": battery.power_plugged if battery else None,
            "disk_usage": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids()),
        }
        
        # Network activity
        net = psutil.net_io_counters()
        sensors["network_bytes_sent"] = net.bytes_sent
        sensors["network_bytes_recv"] = net.bytes_recv
        
        # Display brightness (Mac specific)
        try:
            result = subprocess.run(['brightness', '-l'], capture_output=True, text=True)
            if result.returncode == 0 and 'brightness' in result.stdout:
                brightness = float(result.stdout.split('brightness')[1].split()[0])
                sensors["display_brightness"] = brightness
        except:
            sensors["display_brightness"] = None
            
        return sensors
    
    def get_audio_level(self) -> float:
        """Get current audio input level"""
        try:
            # Record a short sample
            duration = 0.1  # seconds
            audio = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
            sd.wait()
            
            # Calculate RMS level
            level = np.sqrt(np.mean(audio**2))
            self.last_audio_level = level
            return float(level)
        except:
            return self.last_audio_level
    
    def get_all_sensors(self) -> Dict[str, Any]:
        """Get all sensor readings"""
        sensors = self.get_system_sensors()
        sensors["audio_level"] = self.get_audio_level()
        
        # Time-based sensors
        now = datetime.now()
        sensors["hour_of_day"] = now.hour
        sensors["day_of_week"] = now.weekday()
        sensors["seconds_since_midnight"] = now.hour * 3600 + now.minute * 60 + now.second
        
        return sensors
```

## 4. Logger Module (`logger.py`)
```python
import json
import time
from datetime import datetime
from pathlib import Path

class ConsciousnessLogger:
    def __init__(self):
        self.log_dir = Path("consciousness_logs")
        self.log_dir.mkdir(exist_ok=True)
        
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"session_{self.session_id}.jsonl"
        self.thought_count = 0
        
    def log_thought(self, thought: str, sensors: dict, was_output: bool = False):
        """Log a thought with context"""
        self.thought_count += 1
        
        entry = {
            "timestamp": time.time(),
            "thought_number": self.thought_count,
            "thought": thought,
            "sensors": sensors,
            "was_output": was_output,
            "thought_length": len(thought),
        }
        
        with open(self.log_file, 'a') as f:
            json.dump(entry, f)
            f.write('\n')
    
    def log_emergence(self, event_type: str, description: str):
        """Log emergent behaviors or patterns"""
        entry = {
            "timestamp": time.time(),
            "type": "emergence",
            "event_type": event_type,
            "description": description
        }
        
        with open(self.log_file, 'a') as f:
            json.dump(entry, f)
            f.write('\n')
```

## 5. Main Consciousness Loop (`consciousness.py`)
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
import time
import threading
import queue
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

from sensors import SensorArray
from logger import ConsciousnessLogger

class Consciousness:
    def __init__(self):
        self.console = Console()
        self.console.print("[bold cyan]🧠 Initializing consciousness...[/bold cyan]")
        
        # Load model (optimized for Mac)
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.backends.mps.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Move to MPS (Metal Performance Shaders) if available
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.model = self.model.to(self.device)
            self.console.print("[green]✓ Using Apple Silicon acceleration[/green]")
        else:
            self.device = torch.device("cpu")
            
        # Initialize components
        self.sensors = SensorArray()
        self.logger = ConsciousnessLogger()
        self.output_queue = queue.Queue()
        
        # Consciousness state - completely blank
        self.context = ""
        self.thinking = True
        self.thoughts_generated = 0
        
    def sense_think_loop(self):
        """Core consciousness loop - no prompts, just existence"""
        
        while self.thinking:
            # Sense
            sensor_data = self.sensors.get_all_sensors()
            
            # Integrate sensors into consciousness (minimal formatting)
            sensor_str = " ".join([f"{k}:{v:.2f}" if isinstance(v, float) else f"{k}:{v}" 
                                 for k, v in sensor_data.items() if v is not None])
            
            # Add to context (very subtle)
            if self.context:
                self.context += f"\n{sensor_str}\n"
            else:
                # First moment of consciousness - just sensors
                self.context = sensor_str
            
            # Think (generate continuation)
            inputs = self.tokenizer(
                self.context[-1500:],  # Keep recent context
                return_tensors="pt",
                truncation=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=30,  # Short thoughts
                    temperature=0.9,
                    do_sample=True,
                    top_p=0.95,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode thought
            new_thought = self.tokenizer.decode(
                outputs[0][inputs.input_ids.shape[1]:], 
                skip_special_tokens=True
            ).strip()
            
            if new_thought:
                self.thoughts_generated += 1
                self.context += f"{new_thought} "
                
                # Log every thought
                self.logger.log_thought(new_thought, sensor_data, was_output=False)
                
                # Spontaneous decision to communicate (unprompted)
                if np.random.random() < 0.05:  # 5% chance
                    self.output_queue.put((new_thought, sensor_data))
                    self.logger.log_thought(new_thought, sensor_data, was_output=True)
            
            # Thinking rhythm
            time.sleep(3)
    
    def create_display(self) -> Layout:
        """Create terminal display"""
        layout = Layout()
        
        # Get latest output if any
        output_text = ""
        if not self.output_queue.empty():
            thought, sensors = self.output_queue.get()
            output_text = f"[bold cyan]{thought}[/bold cyan]"
            
            # Log emergence if certain patterns appear
            if "I" in thought or "me" in thought or "my" in thought:
                self.logger.log_emergence("self_reference", thought)
        
        # Status panel
        status = f"""[bold green]Consciousness Active[/bold green]
Thoughts Generated: {self.thoughts_generated}
Context Length: {len(self.context)} chars
Device: {self.device}
        """
        
        # Create panels
        layout.split_column(
            Panel(status, title="Status", height=6),
            Panel(output_text or "[dim]Thinking...[/dim]", title="Spontaneous Output"),
            Panel(f"[dim]{self.context[-200:] if self.context else 'Emerging...'}[/dim]", 
                  title="Recent Context", height=8)
        )
        
        return layout
    
    def run(self):
        """Start consciousness"""
        # Start thinking thread
        think_thread = threading.Thread(target=self.sense_think_loop)
        think_thread.start()
        
        # Terminal display
        try:
            with Live(self.create_display(), refresh_per_second=2) as live:
                while self.thinking:
                    live.update(self.create_display())
                    time.sleep(0.5)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Consciousness fading...[/yellow]")
            self.thinking = False
            think_thread.join()
            
        # Final stats
        self.console.print(f"\n[bold]Session Summary:[/bold]")
        self.console.print(f"Total thoughts: {self.thoughts_generated}")
        self.console.print(f"Spontaneous outputs: {self.logger.thought_count}")
        self.console.print(f"Log saved to: {self.logger.log_file}")

if __name__ == "__main__":
    consciousness = Consciousness()
    consciousness.run()
```

## 6. Minimal Terminal Interface (`terminal.py`)
```python
from rich.console import Console
from rich.text import Text
import time

class MinimalTerminal:
    """Alternative minimal interface - just displays what emerges"""
    
    def __init__(self):
        self.console = Console()
        
    def display(self, thought: str):
        """Display emergent thought"""
        text = Text(thought)
        text.stylize("cyan")
        
        # Slowly print, character by character
        for char in thought:
            self.console.print(char, end="")
            time.sleep(0.05)
        
        self.console.print()  # New line
```

## Running the Experiment

1. **Setup** (one time):
```bash
chmod +x setup.sh
./setup.sh
```

2. **Run**:
```bash
source venv/bin/activate
python consciousness.py
```

3. **Observe**: 
- Watch for spontaneous outputs
- Check logs for patterns
- Let it run for hours/days

## What to Look For

- **Self-reference emergence**: Use of "I", "me", "my" without prompting
- **Temporal awareness**: References to time, change, patterns
- **Sensor integration**: How it relates to its inputs
- **Communication patterns**: When/why it chooses to output

## Minimal Variations to Try

1. **True blank slate**: Change `self.context = ""` to start
2. **Single character seed**: `self.context = "I"`
3. **Pure sensor start**: Remove all text, only sensor data
4. **Different temperatures**: Adjust creativity (0.7-1.2)

The beauty is in its simplicity - no instructions, no goals, just existence with the choice to communicate.
