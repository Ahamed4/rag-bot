import os
import logging
import logging.config
from paths import OUTPUTS_DIR

def setup_logger(name='root', console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Configure a universal logger with separate settings for console and file outputs.
    
    Args:
        name: Logger name (use 'root' for the root logger)
        console_level: Logging level for console output (default: INFO)
        file_level: Logging level for file output (default: DEBUG)
    
    Returns:
        Configured logger instance
    """
    # Ensure output directory exists
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    
    # Define logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console_format': {
                'format': '%(levelname)s: %(message)s',  # Simpler format for console
            },
            'file_format': {
                'format': '%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'  # More detailed format for file
            },
        },
        'handlers': {
            'console': {
                'level': console_level,
                'class': 'logging.StreamHandler',
                'formatter': 'console_format'
            },
            'file': {
                'level': file_level,
                'class': 'logging.FileHandler',
                'filename': os.path.join(OUTPUTS_DIR, 'rag_assistant.log'),
                'formatter': 'file_format'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': min(console_level, file_level),  # Set to the more verbose of the two
                'propagate': True
            }
        }
    }
    
    # Configure logging
    logging.config.dictConfig(logging_config)
    return logging.getLogger(name)

# Create default logger instance
logger = setup_logger()

# Example usage:
# logger.debug("Debug message - only goes to file by default")
# logger.info("Info message - goes to both console and file")
# logger.warning("Warning message - goes to both console and file")
# logger.error("Error message - goes to both console and file")