import logging
import os
from datetime import datetime
from typing import Optional

class BankingLogger:
    """Centralized logging configuration for the banking application."""
    
    def __init__(self, log_level: str = "INFO", log_file: Optional[str] = None):
        self.log_level = getattr(logging, log_level.upper())
        self.log_file = log_file or f"logs/bank_app_{datetime.now().strftime('%Y%m%d')}.log"
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging with file and console handlers."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure root logger
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Create application logger
        self.logger = logging.getLogger('BankingApp')
        self.logger.setLevel(self.log_level)
        
        # Log application startup
        self.logger.info("Banking application logging initialized")
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance for a specific module."""
        return logging.getLogger(f'BankingApp.{name}')

# Global logger instance
banking_logger = BankingLogger() 