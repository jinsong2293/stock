"""
Performance monitor cho accessibility features
Theo dõi và tối ưu hiệu suất của hệ thống accessibility

Author: Roo - Architect Mode
Version: 1.0.0
"""

import time
import psutil
import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class PerformanceMetrics:
    """Performance metrics cho accessibility features"""
    timestamp: datetime
    theme_switch_time: float
    contrast_check_time: float
    render_time: float
    memory_usage: float
    cpu_usage: float

class AccessibilityPerformanceMonitor:
    """Monitor performance của accessibility features"""
    
    def __init__(self):
        self.metrics_history: List[PerformanceMetrics] = []
        self.thresholds = {
            'theme_switch': 300,      # milliseconds
            'contrast_check': 10,     # milliseconds
            'render_time': 100,       # milliseconds
            'memory_usage': 100,      # MB
            'cpu_usage': 50          # percentage
        }
    
    def measure_theme_switch(self, func):
        """Decorator để measure theme switching performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Record metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                theme_switch_time=(end_time - start_time) * 1000,  # Convert to ms
                contrast_check_time=0,  # Not applicable here
                render_time=0,  # Not applicable here
                memory_usage=end_memory - start_memory,
                cpu_usage=psutil.cpu_percent()
            )
            
            self.metrics_history.append(metrics)
            
            # Keep only last 100 metrics
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            # Check thresholds
            self._check_performance_thresholds(metrics)
            
            return result
        return wrapper
    
    def measure_contrast_check(self, func):
        """Decorator để measure contrast checking performance"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            
            # Record metrics
            metrics = PerformanceMetrics(
                timestamp=datetime.now(),
                theme_switch_time=0,  # Not applicable here
                contrast_check_time=(end_time - start_time) * 1000,  # Convert to ms
                render_time=0,  # Not applicable here
                memory_usage=0,  # Not applicable here
                cpu_usage=psutil.cpu_percent()
            )
            
            self.metrics_history.append(metrics)
            self._check_performance_thresholds(metrics)
            
            return result
        return wrapper
    
    def _check_performance_thresholds(self, metrics: PerformanceMetrics):
        """Check if metrics exceed thresholds"""
        violations = []
        
        if metrics.theme_switch_time > self.thresholds['theme_switch']:
            violations.append(f"Theme switch time ({metrics.theme_switch_time:.1f}ms) exceeds threshold ({self.thresholds['theme_switch']}ms)")
        
        if metrics.contrast_check_time > self.thresholds['contrast_check']:
            violations.append(f"Contrast check time ({metrics.contrast_check_time:.1f}ms) exceeds threshold ({self.thresholds['contrast_check']}ms)")
        
        if metrics.memory_usage > self.thresholds['memory_usage']:
            violations.append(f"Memory usage ({metrics.memory_usage:.1f}MB) exceeds threshold ({self.thresholds['memory_usage']}MB)")
        
        if metrics.cpu_usage > self.thresholds['cpu_usage']:
            violations.append(f"CPU usage ({metrics.cpu_usage:.1f}%) exceeds threshold ({self.thresholds['cpu_usage']}%)")
        
        # Log violations (in production, send to monitoring service)
        if violations:
            for violation in violations:
                st.warning(f"⚠️ Performance Warning: {violation}")
    
    def get_performance_dashboard(self) -> str:
        """Generate performance dashboard HTML"""
        if not self.metrics_history:
            return "<p>No performance data available yet.</p>"
        
        latest_metrics = self.metrics_history[-1]
        
        # Calculate averages over last 10 measurements
        recent_metrics = self.metrics_history[-10:]
        avg_theme_switch = sum(m.theme_switch_time for m in recent_metrics if m.theme_switch_time > 0) / max(1, len([m for m in recent_metrics if m.theme_switch_time > 0]))
        avg_contrast_check = sum(m.contrast_check_time for m in recent_metrics if m.contrast_check_time > 0) / max(1, len([m for m in recent_metrics if m.contrast_check_time > 0]))
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        
        dashboard_html = f"""
        <div class="performance-dashboard">
            <h3>📊 Performance Metrics</h3>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h4>Theme Switch Time</h4>
                    <div class="metric-value {'good' if latest_metrics.theme_switch_time < self.thresholds['theme_switch'] else 'bad'}">
                        {latest_metrics.theme_switch_time:.1f}ms
                    </div>
                    <div class="metric-avg">Average: {avg_theme_switch:.1f}ms</div>
                </div>
                
                <div class="metric-card">
                    <h4>Contrast Check Time</h4>
                    <div class="metric-value {'good' if latest_metrics.contrast_check_time < self.thresholds['contrast_check'] else 'bad'}">
                        {latest_metrics.contrast_check_time:.1f}ms
                    </div>
                    <div class="metric-avg">Average: {avg_contrast_check:.1f}ms</div>
                </div>
                
                <div class="metric-card">
                    <h4>Memory Usage</h4>
                    <div class="metric-value {'good' if latest_metrics.memory_usage < self.thresholds['memory_usage'] else 'bad'}">
                        {latest_metrics.memory_usage:.1f}MB
                    </div>
                    <div class="metric-avg">Average: {avg_memory:.1f}MB</div>
                </div>
                
                <div class="metric-card">
                    <h4>CPU Usage</h4>
                    <div class="metric-value {'good' if latest_metrics.cpu_usage < self.thresholds['cpu_usage'] else 'bad'}">
                        {latest_metrics.cpu_usage:.1f}%
                    </div>
                    <div class="metric-avg">Current usage</div>
                </div>
            </div>
            
            <div class="performance-status">
                <h4>Status: {'✅ Good' if self._is_performance_good() else '⚠️ Needs Attention'}</h4>
                <p>Last updated: {latest_metrics.timestamp.strftime('%H:%M:%S')}</p>
            </div>
        </div>
        
        <style>
        .performance-dashboard {{
            background: var(--bg_secondary);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}
        
        .metric-card {{
            background: var(--bg_primary);
            border: 1px solid var(--border_primary);
            border-radius: 0.5rem;
            padding: 1rem;
            text-align: center;
        }}
        
        .metric-card h4 {{
            margin: 0 0 0.5rem 0;
            font-size: 0.875rem;
            color: var(--text_secondary);
        }}
        
        .metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }}
        
        .metric-value.good {{
            color: var(--success);
        }}
        
        .metric-value.bad {{
            color: var(--error);
        }}
        
        .metric-avg {{
            font-size: 0.75rem;
            color: var(--text_tertiary);
        }}
        
        .performance-status {{
            text-align: center;
            padding: 1rem;
            background: var(--bg_accent);
            border-radius: 0.5rem;
            margin-top: 1rem;
        }}
        </style>
        """
        
        return dashboard_html
    
    def _is_performance_good(self) -> bool:
        """Check if current performance is within acceptable ranges"""
        if not self.metrics_history:
            return True
        
        latest = self.metrics_history[-1]
        
        return (
            latest.theme_switch_time <= self.thresholds['theme_switch'] and
            latest.contrast_check_time <= self.thresholds['contrast_check'] and
            latest.memory_usage <= self.thresholds['memory_usage'] and
            latest.cpu_usage <= self.thresholds['cpu_usage']
        )
    
    def export_metrics(self) -> str:
        """Export metrics as JSON"""
        metrics_data = []
        for metric in self.metrics_history:
            metrics_data.append({
                'timestamp': metric.timestamp.isoformat(),
                'theme_switch_time': metric.theme_switch_time,
                'contrast_check_time': metric.contrast_check_time,
                'render_time': metric.render_time,
                'memory_usage': metric.memory_usage,
                'cpu_usage': metric.cpu_usage
            })
        
        return json.dumps(metrics_data, indent=2)
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary for last 24 hours"""
        if not self.metrics_history:
            return {
                'status': 'no_data',
                'message': 'No performance data available'
            }
        
        # Filter metrics from last 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        
        if not recent_metrics:
            return {
                'status': 'no_recent_data',
                'message': 'No performance data from last 24 hours'
            }
        
        # Calculate summary statistics
        theme_switches = [m for m in recent_metrics if m.theme_switch_time > 0]
        contrast_checks = [m for m in recent_metrics if m.contrast_check_time > 0]
        
        summary = {
            'status': 'good' if self._is_performance_good() else 'warning',
            'time_range': '24 hours',
            'total_measurements': len(recent_metrics),
            'theme_switches': len(theme_switches),
            'contrast_checks': len(contrast_checks),
            'performance': {
                'avg_theme_switch_time': sum(m.theme_switch_time for m in theme_switches) / len(theme_switches) if theme_switches else 0,
                'avg_contrast_check_time': sum(m.contrast_check_time for m in contrast_checks) / len(contrast_checks) if contrast_checks else 0,
                'avg_memory_usage': sum(m.memory_usage for m in recent_metrics) / len(recent_metrics),
                'avg_cpu_usage': sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
            },
            'thresholds': self.thresholds,
            'violations': self._get_recent_violations(recent_metrics)
        }
        
        return summary
    
    def _get_recent_violations(self, metrics: List[PerformanceMetrics]) -> List[Dict]:
        """Get performance violations from recent metrics"""
        violations = []
        
        for metric in metrics:
            if metric.theme_switch_time > self.thresholds['theme_switch']:
                violations.append({
                    'type': 'theme_switch',
                    'value': metric.theme_switch_time,
                    'threshold': self.thresholds['theme_switch'],
                    'timestamp': metric.timestamp.isoformat()
                })
            
            if metric.contrast_check_time > self.thresholds['contrast_check']:
                violations.append({
                    'type': 'contrast_check',
                    'value': metric.contrast_check_time,
                    'threshold': self.thresholds['contrast_check'],
                    'timestamp': metric.timestamp.isoformat()
                })
            
            if metric.memory_usage > self.thresholds['memory_usage']:
                violations.append({
                    'type': 'memory_usage',
                    'value': metric.memory_usage,
                    'threshold': self.thresholds['memory_usage'],
                    'timestamp': metric.timestamp.isoformat()
                })
            
            if metric.cpu_usage > self.thresholds['cpu_usage']:
                violations.append({
                    'type': 'cpu_usage',
                    'value': metric.cpu_usage,
                    'threshold': self.thresholds['cpu_usage'],
                    'timestamp': metric.timestamp.isoformat()
                })
        
        return violations
    
    def clear_metrics(self):
        """Clear all stored metrics"""
        self.metrics_history.clear()
    
    def update_thresholds(self, new_thresholds: Dict):
        """Update performance thresholds"""
        self.thresholds.update(new_thresholds)

# Global performance monitor instance
performance_monitor = AccessibilityPerformanceMonitor()