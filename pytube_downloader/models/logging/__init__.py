from structlog.stdlib import BoundLogger, LoggerFactory
from .logger import Logger
from .formatter import FormatterFactory
import structlog

_loggerFactory = LoggerFactory()
def configure_one(wrapper_class=BoundLogger,logger_factory=None,processors=FormatterFactory.processors):
    structlog.reset_defaults()
    structlog.configure_once(wrapper_class=wrapper_class
                            ,logger_factory=logger_factory if logger_factory else _loggerFactory,
                            processors=processors)

def info(msg):
    logger = Logger.getRootLogger()
    logger.info(msg)
    
def getLogger(name="",level=0):
    """ Get the python logging.Logger which has filehandler to generate log file. The log will print on console by root Logger instead of this logger.

        Args:
            name (str, optional): the logger name, usually use the ``__name__`` for moduel of ``__name__.function``. Defaults to ``root``.
            level (int, optional): level = 0 is the lowest level to pass all log to log record. U can use ``logging.INFO``, ``logging.DEBUG``, ``logging.WARN`` 
            and ``logging.ERROR``.Defaults to 0.

        Returns:
            logging.Logger: The the singleton logger with the name of module
    """        
    return Logger.getLogger(name,level)