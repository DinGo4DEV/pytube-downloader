import logging

from logging.handlers import QueueListener, TimedRotatingFileHandler,QueueHandler

from structlog.types import EventDict
import sys
from pathlib import Path
import structlog
from structlog.stdlib import LoggerFactory,AsyncBoundLogger,BoundLogger
from structlog.processors import JSONRenderer, ExceptionPrettyPrinter,UnicodeDecoder,TimeStamper,format_exc_info,KeyValueRenderer,CallsiteParameterAdder,CallsiteParameter

LOG_RECORD_ATTRIBUTES = {
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'message', 'module',
    'msecs', 'msg', 'name', 'pathname', 'process', 'processName',
    'relativeCreated', 'stack_info', 'thread', 'threadName',
    }

def extract_stdlib_extra(logger, method_name, event_dict):
        """
        Extract the `extra` key-values from the standard logger record
        and populate the `event_dict` with them.
        """
        record_extra = {k: v for k, v in vars(event_dict['_record']).items()
                        if k not in LOG_RECORD_ATTRIBUTES}
        event_dict.update(record_extra)
        return event_dict
    
def format_structlog_event(logger: logging.Logger,__:str,event_dict: EventDict):
    msg = event_dict.pop("event")
    event_dict.update({"message":msg})
    return event_dict


class OrderJsonKey(KeyValueRenderer):
    def __call__(self, _, __: str, event_dict: EventDict):
        return { k: v for k, v in self._ordered_items(event_dict)}

class FormatterFactory(structlog.stdlib.ProcessorFormatter):
    """Logger Formatter Factory, External Logging format for python built-in logger.
        
    Args:
        processors (list): structlog's processor when out-put log
        foreign_pre_chain 
    """
    processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    format_structlog_event,
                    # structlog.stdlib.render_to_log_kwargs,
                    # JSONRenderer( sort_keys=True,ensure_ascii=False),
                    KeyValueRenderer(sort_keys=True,key_order=["timestamp","level","logger","message","exception"],drop_missing=True)
                ]
    shared_processors = [
                structlog.threadlocal.merge_threadlocal,
                ## Add logger name to log entry
                structlog.stdlib.add_logger_name,
                ## Add logger name to log level
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                                 
                # TimeStamper(fmt="%Y-%m-%d %H:%M:%S",utc=False,key="timestamp"),
                TimeStamper(fmt="iso",utc=True,key="timestamp"),
                CallsiteParameterAdder([CallsiteParameter.LINENO,CallsiteParameter.FILENAME,CallsiteParameter.FUNC_NAME,CallsiteParameter.MODULE]),
                UnicodeDecoder(),                 
                format_exc_info,
                extract_stdlib_extra,
                
    ]
    def __init__(self,processors=None,foreign_pre_chain=None,*args,**kwargs):
        if processors is None:
            format= kwargs.get("format","json")            
            processors = FormatterFactory.processors
            if format and format == "json":
                kwargs.pop("format")
                processors.pop(-1)
                processors+= [OrderJsonKey(sort_keys=True,key_order=["timestamp","level","logger","message","exception"],drop_missing=True),
                              JSONRenderer( sort_keys=False,ensure_ascii=False)]
        if foreign_pre_chain is None:            
            foreign_pre_chain = FormatterFactory.shared_processors
            
                
        super().__init__(processors=processors,foreign_pre_chain=foreign_pre_chain,*args,**kwargs)
        pass