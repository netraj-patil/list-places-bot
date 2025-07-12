import logging
import functools

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def logging_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Called Function: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function: {func.__name__} Returned: {result}")
            return result
        except Exception as e:
            logger.exception(f"Error in Function {func.__name__}: {e} ")
            raise
    return wrapper
