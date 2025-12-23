"""
Configuration Management System cho Stock Analyzer
Simple configuration với environment variables support
"""

import os
import json
from typing import Dict, Any, Optional


class StockAnalyzerConfig:
    """
    Simple configuration manager cho Stock Analyzer
    """
    
    # Default configuration
    _defaults = {
        # Database Configuration
        "DATABASE_URL": "sqlite:///./stock_analyzer.db",
        "CACHE_DIR": "cache",
        
        # API Configuration
        "GOOGLE_API_KEY": "",
        "ALPHA_VANTAGE_API_KEY": "",
        "NEWS_API_KEY": "",
        
        # Performance Configuration
        "MAX_WORKERS": 10,
        "BATCH_SIZE": 20,
        "REQUEST_TIMEOUT": 30,
        "MAX_RETRIES": 3,
        
        # Cache Configuration
        "USE_CACHE": True,
        "CACHE_TTL_TECHNICAL": 1800,  # 30 minutes
        "CACHE_TTL_SENTIMENT": 7200,  # 2 hours
        "CACHE_TTL_FINANCIAL": 86400,  # 24 hours
        "CACHE_TTL_MARKET": 300,  # 5 minutes
        
        # Analysis Configuration
        "DEFAULT_LOOKBACK_DAYS": 365,
        "MIN_CONFIDENCE_SCORE": 60.0,
        "MAX_CONCURRENT_ANALYSES": 5,
        
        # Technical Analysis Parameters
        "RSI_WINDOW": 14,
        "MACD_FAST": 12,
        "MACD_SLOW": 26,
        "MACD_SIGNAL": 9,
        "BB_WINDOW": 20,
        "BB_STD_DEV": 2.0,
        "ATR_WINDOW": 14,
        
        # Smart Money Detection Parameters
        "SMART_MONEY_VOLUME_RATIO": 1.8,
        "SMART_MONEY_PRICE_CHANGE_PCT": 1.0,
        "SMART_MONEY_LOOKBACK_DAYS": 60,
        "SMART_MONEY_MIN_CONFIDENCE": 60,
        "SMART_MONEY_MAX_RSI": 80,
        
        # Risk Management Parameters
        "DEFAULT_COMMISSION_RATE": 0.0015,
        "DEFAULT_SLIPPAGE_RATE": 0.0005,
        "MAX_POSITION_SIZE_PCT": 10.0,
        
        # UI Configuration
        "THEME": "dark",
        "CHART_HEIGHT": 500,
        "TABLE_MAX_ROWS": 1000,
        "MOBILE_BREAKPOINT": 768,
        
        # Logging Configuration
        "LOG_LEVEL": "INFO",
        "LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "ENABLE_FILE_LOGGING": True,
        "LOG_FILE_PATH": "logs/stock_analyzer.log",
        
        # Development Configuration
        "DEBUG": False,
        "DEVELOPMENT_MODE": False,
        "MOCK_DATA": False,
        
        # Notification Configuration
        "ENABLE_NOTIFICATIONS": True,
        "EMAIL_NOTIFICATIONS": False,
        "NOTIFICATION_EMAIL": ""
    }
    
    def __init__(self):
        self._config = self._defaults.copy()
        self._load_from_environment()
        self._load_from_file()
    
    def _load_from_environment(self):
        """Load configuration từ environment variables"""
        for key in self._defaults:
            env_value = os.getenv(key)
            if env_value is not None:
                # Convert to appropriate type
                self._config[key] = self._convert_value(env_value, self._defaults[key])
    
    def _load_from_file(self):
        """Load configuration từ file"""
        config_file = ".env"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                key = key.strip()
                                value = value.strip()
                                if key in self._defaults:
                                    self._config[key] = self._convert_value(value, self._defaults[key])
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _convert_value(self, value: str, default_value: Any) -> Any:
        """Convert string value to appropriate type"""
        if isinstance(default_value, bool):
            return value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(default_value, int):
            try:
                return int(value)
            except ValueError:
                return default_value
        elif isinstance(default_value, float):
            try:
                return float(value)
            except ValueError:
                return default_value
        else:
            return value
    
    def get(self, key: str, default=None) -> Any:
        """Lấy configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        if key in self._defaults:
            self._config[key] = value
        else:
            raise ValueError(f"Unknown configuration key: {key}")
    
    def get_all(self) -> Dict[str, Any]:
        """Lấy tất cả configuration"""
        return self._config.copy()
    
    def get_category(self, category: str) -> Dict[str, Any]:
        """Lấy configuration theo category"""
        category_map = {
            "database": ["DATABASE_URL", "CACHE_DIR"],
            "performance": ["MAX_WORKERS", "BATCH_SIZE", "REQUEST_TIMEOUT", "MAX_RETRIES", "MAX_CONCURRENT_ANALYSES"],
            "cache": ["USE_CACHE", "CACHE_TTL_TECHNICAL", "CACHE_TTL_SENTIMENT", "CACHE_TTL_FINANCIAL", "CACHE_TTL_MARKET"],
            "technical_indicators": ["RSI_WINDOW", "MACD_FAST", "MACD_SLOW", "MACD_SIGNAL", "BB_WINDOW", "BB_STD_DEV", "ATR_WINDOW"],
            "smart_money": ["SMART_MONEY_VOLUME_RATIO", "SMART_MONEY_PRICE_CHANGE_PCT", "SMART_MONEY_LOOKBACK_DAYS", "SMART_MONEY_MIN_CONFIDENCE", "SMART_MONEY_MAX_RSI"],
            "risk_management": ["DEFAULT_COMMISSION_RATE", "DEFAULT_SLIPPAGE_RATE", "MAX_POSITION_SIZE_PCT"],
            "ui": ["THEME", "CHART_HEIGHT", "TABLE_MAX_ROWS", "MOBILE_BREAKPOINT"],
            "logging": ["LOG_LEVEL", "LOG_FORMAT", "ENABLE_FILE_LOGGING", "LOG_FILE_PATH"],
            "development": ["DEBUG", "DEVELOPMENT_MODE", "MOCK_DATA"],
            "notifications": ["ENABLE_NOTIFICATIONS", "EMAIL_NOTIFICATIONS", "NOTIFICATION_EMAIL"]
        }
        
        if category not in category_map:
            raise ValueError(f"Invalid category: {category}")
        
        return {key: self._config[key] for key in category_map[category]}
    
    def export_template(self, file_path: str = ".env.template"):
        """Export configuration template"""
        template_lines = []
        template_lines.append("# Stock Analyzer Configuration Template")
        template_lines.append("# Copy this file to .env and update values")
        template_lines.append("")
        
        for key, default_value in self._defaults.items():
            template_lines.append(f"# {key} (default: {default_value})")
            template_lines.append(f"{key}={default_value}")
            template_lines.append("")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(template_lines))
    
    def save_to_file(self, file_path: str = ".env"):
        """Save current configuration to file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            for key, value in self._config.items():
                f.write(f"{key}={value}\n")


# Global configuration instance
_config = None

def get_config() -> StockAnalyzerConfig:
    """Lấy global configuration instance"""
    global _config
    if _config is None:
        _config = StockAnalyzerConfig()
    return _config


# Convenience functions
def get_database_config() -> Dict[str, Any]:
    """Lấy database configuration"""
    return get_config().get_category("database")


def get_performance_config() -> Dict[str, Any]:
    """Lấy performance configuration"""
    return get_config().get_category("performance")


def get_cache_config() -> Dict[str, Any]:
    """Lấy cache configuration"""
    return get_config().get_category("cache")


def get_technical_indicators_config() -> Dict[str, Any]:
    """Lấy technical indicators configuration"""
    return get_config().get_category("technical_indicators")


def get_smart_money_config() -> Dict[str, Any]:
    """Lấy smart money configuration"""
    return get_config().get_category("smart_money")


def get_risk_management_config() -> Dict[str, Any]:
    """Lấy risk management configuration"""
    return get_config().get_category("risk_management")


def get_ui_config() -> Dict[str, Any]:
    """Lấy UI configuration"""
    return get_config().get_category("ui")


def get_logging_config() -> Dict[str, Any]:
    """Lấy logging configuration"""
    return get_config().get_category("logging")


def get_setting(key: str, default=None):
    """Lấy individual setting"""
    return get_config().get(key, default)


def set_setting(key: str, value: Any):
    """Set individual setting"""
    get_config().set(key, value)


if __name__ == "__main__":
    # Test configuration system
    config = StockAnalyzerConfig()
    
    print("Current Configuration:")
    for key, value in config.get_all().items():
        print(f"  {key}: {value}")
    
    print("\nDatabase Config:")
    db_config = get_database_config()
    for key, value in db_config.items():
        print(f"  {key}: {value}")
    
    print("\nPerformance Config:")
    perf_config = get_performance_config()
    for key, value in perf_config.items():
        print(f"  {key}: {value}")
    
    # Export template
    config.export_template()
    print("\nConfiguration template exported to .env.template")