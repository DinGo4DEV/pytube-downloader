import queue
import logging

from logging.handlers import QueueListener, TimedRotatingFileHandler,QueueHandler
import sys
from pathlib import Path
import structlog
from structlog.stdlib import LoggerFactory,AsyncBoundLogger,BoundLogger
from pythonjsonlogger import jsonlogger
import formatter
    
    # def format(self, record: logging.LogRecord) -> str:
    #     return super().format(record=record)
    
class Logger:
    """ Class Logger using built-in logger and structlog"""
    LOG_RECORD_ATTRIBUTES = {
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'message', 'module',
    'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
    'relativeCreated', 'stack_info', 'thread', 'threadName',
    }
    
    ## If using asyncio framework "Fastapi" Use AsyncBoundLogger for wrapper
    # structlog.configure_once(wrapper_class=BoundLogger
    #                         ,logger_factory=LoggerFactory(),
    #                         processors=formatter.FormatterFactory.processors)

    root = logging.getLogger()
    root.setLevel(0)
    # file_utils.check_and_create_directory('log')

    @staticmethod
    def getRootLogger(format_json=True,file_path=None) -> logging.Logger:
        """
        Get the default logger root, with 3 handlers (console, file, queue (mutil-thread))
        The root logger will print all the logging level as it is set to 0. 
        Therefore, other logger do not need to print on console

        Args:
            file_path (Path,optional): the log file path (e.g `Path("log/")`)

        Returns:
            logging.Logger: [logging.Logger] which has formatted console log and create plain text & json log on `path`
        """        
        root = Logger.root
        if len(root.handlers)<1:
            Logger.add_console_handler(root,format_json)
            if file_path: Logger.add_file_handler(root,root.name,level=logging.INFO,file_path=file_path)
            # Logger.add_queue_handler(root,format_json)
        return Logger.root
    
    @staticmethod
    def getLogger(name="",level=0, format_json=True, file_path:Path=None) -> logging.Logger:
        """ Get the python logging.Logger which has filehandler to generate log file. The log will print on console by root Logger instead of this logger.

        Args:
            name (str, optional): the logger name, usually use the ``__name__`` for moduel of ``__name__.function``. Defaults to ``root``.
            level (int, optional): level = 0 is the lowest level to pass all log to log record. U can use ``logging.INFO``, ``logging.DEBUG``, ``logging.WARN`` and ``logging.ERROR``.Defaults to 0.
            format_json (bool, optional): `True` for output external json format on log directory, `False` will only output the plain text log.
            file_path (Path,optional): the log file path (e.g `Path("log/")`)

        Returns:
            logging.Logger: The the singleton logger with the name of module
        """        
        if name == "": return Logger.getRootLogger()
        logger = logging.getLogger(name)
        if logger.level != level: logger.setLevel(level)
        if len(logger.handlers)<1 and len(Logger.root.handlers) < 1:
            if file_path:
                Logger.add_file_handler(logger,name,level=level,file_path=file_path)
            Logger.add_console_handler(logger,level,format_json)
        return logger
    
    
    @staticmethod
    def add_console_handler(logger:logging.Logger=None,level=logging.INFO,format_json=True):
        # formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] [%(process)d - %(processName)s] : %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(formatter.FormatterFactory(format="json" if format_json else None))
        logger.addHandler(handler)
        logger.propagate = False
        return handler
    
    @staticmethod
    def add_file_handler(logger: logging.Logger,filename, level=logging.ERROR,file_path=Path("log/")):
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] [%(process)d - %(processName)s] : %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        # handler = TimedRotatingFileHandler(filename=Path(config['logging']['path']),encoding="utf-8",when="W0")
        handler = TimedRotatingFileHandler(filename=file_path.joinpath(Path(filename+".log")),encoding="utf-8",when="W0")
        handler.setLevel(level)
        handler.setFormatter(Logger.formatter)
        logger.addHandler(handler)
        return handler
    
    @staticmethod
    def add_queue_handler(logger: logging.Logger,format_json):
        from queue import Queue
        # formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] [%(process)d - %(processName)s] : %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        queue=Queue()
        handler = QueueHandler(queue)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter.FormatterFactory(format="json" if format_json else None))
        # handler.set_name()
        logger.addHandler(handler)
        QueueListener(queue,*logger.handlers,True)
        return queue