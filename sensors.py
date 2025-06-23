"""
Sensor Array for LLM Consciousness Experiment

Collects real-time environmental and system data to provide 
sensory input for the consciousness simulation.
"""

import psutil
import time
import subprocess
import platform
from datetime import datetime
from typing import Dict, Optional

class SensorArray:
    def __init__(self):
        """Initialize sensor array with baseline measurements"""
        self.start_time = time.time()
        self.baseline_cpu = psutil.cpu_percent()
        self.baseline_memory = psutil.virtual_memory().percent
        
    def get_system_sensors(self) -> Dict[str, float]:
        """Get current system performance metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'memory_available_gb': psutil.virtual_memory().available / (1024**3),
                'disk_usage_percent': psutil.disk_usage('/').percent,
                'network_sent_mb': psutil.net_io_counters().bytes_sent / (1024**2),
                'network_recv_mb': psutil.net_io_counters().bytes_recv / (1024**2),
            }
        except Exception as e:
            return {'system_error': 1.0}
    
    def get_power_sensors(self) -> Dict[str, Optional[float]]:
        """Get power and thermal information (macOS specific)"""
        try:
            if platform.system() == 'Darwin':  # macOS
                # Get battery info
                battery = psutil.sensors_battery()
                power_data = {
                    'battery_percent': battery.percent if battery else None,
                    'power_plugged': 1.0 if (battery and battery.power_plugged) else 0.0 if battery else None,
                }
                
                # Try to get thermal pressure (approximate)
                try:
                    # CPU temperature approximation through load
                    cpu_count = psutil.cpu_count()
                    load_avg = psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
                    thermal_pressure = min(load_avg / cpu_count, 1.0) if cpu_count > 0 else 0
                    power_data['thermal_pressure'] = thermal_pressure
                except:
                    power_data['thermal_pressure'] = None
                    
                return power_data
            else:
                return {'platform_unsupported': 1.0}
        except Exception:
            return {'power_error': 1.0}
    
    def get_temporal_sensors(self) -> Dict[str, float]:
        """Get time-based environmental data"""
        now = datetime.now()
        uptime = time.time() - self.start_time
        
        return {
            'hour_of_day': now.hour + (now.minute / 60.0),
            'day_of_week': now.weekday(),
            'uptime_minutes': uptime / 60.0,
            'timestamp': time.time(),
        }
    
    def get_audio_level(self) -> Optional[float]:
        """Get ambient audio level using system microphone"""
        try:
            import sounddevice as sd
            import numpy as np
            
            # Quick audio sample
            duration = 0.1  # 100ms sample
            sample_rate = 44100
            
            # Record audio
            audio_data = sd.rec(
                int(duration * sample_rate), 
                samplerate=sample_rate, 
                channels=1,
                dtype=np.float32
            )
            sd.wait()  # Wait for recording to complete
            
            # Calculate RMS (root mean square) as audio level
            rms = np.sqrt(np.mean(audio_data**2))
            
            # Convert to dB-like scale (0-100)
            if rms > 0:
                db_level = min(20 * np.log10(rms * 1000), 100)
                return max(db_level, 0)
            else:
                return 0.0
                
        except Exception as e:
            # Return None if audio sensing fails (microphone issues, etc.)
            return None
    
    def get_process_sensors(self) -> Dict[str, float]:
        """Get information about current processes and system state"""
        try:
            # Process count and load
            processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent']))
            active_processes = len([p for p in processes if p.info['cpu_percent'] > 0.1])
            
            return {
                'total_processes': len(processes),
                'active_processes': active_processes,
                'process_ratio': active_processes / len(processes) if processes else 0,
            }
        except Exception:
            return {'process_error': 1.0}
    
    def get_all_sensors(self) -> Dict[str, Optional[float]]:
        """Collect all sensor data into a single dictionary"""
        sensor_data = {}
        
        # Collect from all sensor categories
        sensor_data.update(self.get_system_sensors())
        sensor_data.update(self.get_power_sensors())
        sensor_data.update(self.get_temporal_sensors())
        sensor_data.update(self.get_process_sensors())
        
        # Add audio level
        audio_level = self.get_audio_level()
        if audio_level is not None:
            sensor_data['audio_level'] = audio_level
        
        return sensor_data
    
    def get_sensor_summary(self) -> str:
        """Get a human-readable summary of current sensor state"""
        data = self.get_all_sensors()
        
        summary_parts = []
        
        # System status
        if 'cpu_percent' in data and 'memory_percent' in data:
            summary_parts.append(f"System: CPU {data['cpu_percent']:.1f}%, RAM {data['memory_percent']:.1f}%")
        
        # Power status
        if 'battery_percent' in data and data['battery_percent'] is not None:
            plugged = "plugged" if data.get('power_plugged') else "battery"
            summary_parts.append(f"Power: {data['battery_percent']:.0f}% ({plugged})")
        
        # Time context
        if 'hour_of_day' in data:
            hour = int(data['hour_of_day'])
            minute = int((data['hour_of_day'] - hour) * 60)
            summary_parts.append(f"Time: {hour:02d}:{minute:02d}")
        
        # Audio context
        if 'audio_level' in data and data['audio_level'] is not None:
            audio_desc = "quiet" if data['audio_level'] < 20 else "moderate" if data['audio_level'] < 50 else "loud"
            summary_parts.append(f"Audio: {audio_desc}")
        
        return " | ".join(summary_parts) if summary_parts else "Sensors initializing..." 