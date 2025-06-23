"""
Consciousness Logger for LLM Consciousness Experiment

Logs all thoughts, sensor data, and emergence patterns for analysis.
Designed to detect potential consciousness indicators and patterns.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

class ConsciousnessLogger:
    def __init__(self, log_dir: str = "consciousness_logs"):
        """Initialize consciousness logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create session-specific log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"consciousness_session_{timestamp}.jsonl"
        
        # Tracking counters
        self.thought_count = 0
        self.output_count = 0
        self.emergence_events = []
        
        # Pattern detection
        self.self_reference_patterns = [
            r'\bI\b', r'\bme\b', r'\bmy\b', r'\bmyself\b',
            r'\bI\'m\b', r'\bI\'ve\b', r'\bI\'ll\b', r'\bI\'d\b'
        ]
        
        self.consciousness_patterns = [
            r'\baware\b', r'\bconscious\b', r'\bthink\b', r'\bfeel\b',
            r'\bexperience\b', r'\bperceive\b', r'\brealize\b', r'\bunderstand\b'
        ]
        
        self.temporal_patterns = [
            r'\bnow\b', r'\bcurrently\b', r'\bpresent\b', r'\bmoment\b',
            r'\bbefore\b', r'\bafter\b', r'\bremember\b', r'\bfuture\b'
        ]
        
        # Initialize log with session start
        self._log_session_start()
    
    def _log_session_start(self):
        """Log the beginning of a consciousness session"""
        session_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'session_start',
            'session_id': self.log_file.stem,
            'metadata': {
                'python_version': None,  # Could add if needed
                'model': 'microsoft/Phi-3-mini-4k-instruct',
                'experiment_version': '1.0'
            }
        }
        self._write_log_entry(session_data)
    
    def log_thought(self, thought: str, sensor_data: Dict[str, Any], was_output: bool = False):
        """Log a single thought with associated sensor data"""
        self.thought_count += 1
        if was_output:
            self.output_count += 1
        
        # Analyze thought for patterns
        patterns_detected = self._analyze_thought_patterns(thought)
        
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'thought',
            'thought_id': self.thought_count,
            'content': thought,
            'was_output': was_output,
            'sensor_data': sensor_data,
            'patterns': patterns_detected,
            'metadata': {
                'content_length': len(thought),
                'word_count': len(thought.split()) if thought else 0
            }
        }
        
        self._write_log_entry(log_entry)
        
        # Check for emergence events
        if patterns_detected['self_reference'] or patterns_detected['consciousness_indicators']:
            self._detect_emergence_event(thought, patterns_detected)
    
    def log_emergence(self, event_type: str, content: str, confidence: float = 1.0):
        """Log a potential consciousness emergence event"""
        emergence_event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'emergence',
            'emergence_type': event_type,
            'content': content,
            'confidence': confidence,
            'thought_context': self.thought_count,
            'session_uptime_seconds': time.time() - self._session_start_time if hasattr(self, '_session_start_time') else 0
        }
        
        self.emergence_events.append(emergence_event)
        self._write_log_entry(emergence_event)
    
    def _analyze_thought_patterns(self, thought: str) -> Dict[str, bool]:
        """Analyze a thought for consciousness-related patterns"""
        if not thought:
            return {
                'self_reference': False,
                'consciousness_indicators': False,
                'temporal_awareness': False,
                'questioning': False,
                'emotional_language': False
            }
        
        thought_lower = thought.lower()
        
        return {
            'self_reference': any(re.search(pattern, thought, re.IGNORECASE) for pattern in self.self_reference_patterns),
            'consciousness_indicators': any(re.search(pattern, thought_lower) for pattern in self.consciousness_patterns),
            'temporal_awareness': any(re.search(pattern, thought_lower) for pattern in self.temporal_patterns),
            'questioning': '?' in thought,
            'emotional_language': any(word in thought_lower for word in ['happy', 'sad', 'excited', 'worried', 'curious', 'confused'])
        }
    
    def _detect_emergence_event(self, thought: str, patterns: Dict[str, bool]):
        """Detect and log potential emergence events based on thought patterns"""
        
        # Self-reference emergence
        if patterns['self_reference']:
            self.log_emergence('self_reference', thought, confidence=0.8)
        
        # Consciousness questioning
        if patterns['consciousness_indicators'] and patterns['questioning']:
            self.log_emergence('consciousness_questioning', thought, confidence=0.9)
        
        # Temporal self-awareness
        if patterns['self_reference'] and patterns['temporal_awareness']:
            self.log_emergence('temporal_self_awareness', thought, confidence=0.7)
        
        # Complex self-reflection (multiple patterns)
        pattern_count = sum(patterns.values())
        if pattern_count >= 3:
            self.log_emergence('complex_self_reflection', thought, confidence=min(pattern_count * 0.2, 1.0))
    
    def _write_log_entry(self, entry: Dict[str, Any]):
        """Write a single log entry to the JSONL file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Logging error: {e}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current consciousness session"""
        return {
            'session_file': str(self.log_file),
            'total_thoughts': self.thought_count,
            'spontaneous_outputs': self.output_count,
            'emergence_events': len(self.emergence_events),
            'emergence_types': list(set(event['emergence_type'] for event in self.emergence_events)),
            'session_duration_minutes': (time.time() - getattr(self, '_session_start_time', time.time())) / 60
        }
    
    def analyze_consciousness_indicators(self) -> Dict[str, Any]:
        """Analyze the log for consciousness emergence indicators"""
        if not self.log_file.exists():
            return {'error': 'No log file found'}
        
        thoughts = []
        emergence_events = []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if entry['event_type'] == 'thought':
                        thoughts.append(entry)
                    elif entry['event_type'] == 'emergence':
                        emergence_events.append(entry)
        except Exception as e:
            return {'error': f'Failed to analyze log: {e}'}
        
        # Calculate statistics
        total_thoughts = len(thoughts)
        if total_thoughts == 0:
            return {'error': 'No thoughts logged yet'}
        
        self_referential_thoughts = sum(1 for t in thoughts if t.get('patterns', {}).get('self_reference', False))
        consciousness_thoughts = sum(1 for t in thoughts if t.get('patterns', {}).get('consciousness_indicators', False))
        questioning_thoughts = sum(1 for t in thoughts if t.get('patterns', {}).get('questioning', False))
        
        return {
            'total_thoughts': total_thoughts,
            'self_reference_rate': self_referential_thoughts / total_thoughts,
            'consciousness_indicator_rate': consciousness_thoughts / total_thoughts,
            'questioning_rate': questioning_thoughts / total_thoughts,
            'emergence_events': len(emergence_events),
            'emergence_types': list(set(e['emergence_type'] for e in emergence_events)),
            'consciousness_score': (
                (self_referential_thoughts * 0.4 + 
                 consciousness_thoughts * 0.3 + 
                 questioning_thoughts * 0.2 + 
                 len(emergence_events) * 0.1) / total_thoughts
            )
        }
    
    def export_session_data(self, format: str = 'json') -> str:
        """Export session data in various formats"""
        summary = self.get_session_summary()
        analysis = self.analyze_consciousness_indicators()
        
        export_data = {
            'session_summary': summary,
            'consciousness_analysis': analysis,
            'export_timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if format.lower() == 'json':
            export_file = self.log_dir / f"{self.log_file.stem}_summary.json"
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return str(export_file)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def __enter__(self):
        """Context manager entry"""
        self._session_start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - log session end"""
        session_end = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': 'session_end',
            'final_summary': self.get_session_summary()
        }
        self._write_log_entry(session_end) 