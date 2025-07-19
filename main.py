#!/usr/bin/env python3
"""
Main entry point for Ted Sink Law Voice Receptionist AI
"""
import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.main import app
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/ted_sink_law_ai.log') if os.path.exists('/var/log') else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    import uvicorn
    
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Firm: {settings.firm_name}")
    logger.info(f"Service states: {', '.join(settings.service_states)}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    # Run the FastAPI application
    uvicorn.run(
        "backend.main:app",
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8000)),
        reload=os.getenv('DEBUG', 'false').lower() == 'true',
        log_level=os.getenv('LOG_LEVEL', 'info'),
        access_log=True
    )

if __name__ == "__main__":
    main()