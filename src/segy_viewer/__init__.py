"""
Segy Viewer
===========

Desktop application for SEG-Y file inspection and analysis.
"""
from .config import AppConfig

__version__ = AppConfig.app_version

__all__ = ["AppConfig"]