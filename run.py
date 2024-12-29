import os
import sys
import asyncio
import logging
from src.utils.logging import setup_logger

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logger = setup_logger("consensus_runner", level=logging.INFO)

async def main():
    try:
        from src.main import test_consensus_system
        await test_consensus_system()
    except Exception as e:
        logger.error(f"Error running consensus system: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1) 