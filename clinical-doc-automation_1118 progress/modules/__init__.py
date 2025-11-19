"""
Clinical Document Automation - Modules Package

此包包含各種臨床文件自動化處理模組
"""

try:
    from .protocol_parser import ProtocolParser, ProtocolInfo as ProtocolInfoParser
    _PROTOCOL_PARSER_AVAILABLE = True
except ImportError:
    _PROTOCOL_PARSER_AVAILABLE = False

try:
    from .user_guide_generator import UserGuideGenerator, ScreenshotPlaceholder
    _USER_GUIDE_AVAILABLE = True
except ImportError:
    _USER_GUIDE_AVAILABLE = False

try:
    from .dvp_generator import (
        DVPGenerator,
        ProtocolInfo,
        CRFField,
        ValidationRule,
        Severity,
        ValidationType,
        create_dvp
    )
    _DVP_GENERATOR_AVAILABLE = True
except ImportError:
    _DVP_GENERATOR_AVAILABLE = False

__all__ = []

if _PROTOCOL_PARSER_AVAILABLE:
    __all__.extend(['ProtocolParser', 'ProtocolInfoParser'])

if _USER_GUIDE_AVAILABLE:
    __all__.extend(['UserGuideGenerator', 'ScreenshotPlaceholder'])

if _DVP_GENERATOR_AVAILABLE:
    __all__.extend([
        'DVPGenerator',
        'ProtocolInfo',
        'CRFField',
        'ValidationRule',
        'Severity',
        'ValidationType',
        'create_dvp'
    ])
__version__ = '1.0.0'
