"""
Qishloq Xo'jaligi Roboti - Interaktiv Maydon Planner
====================================================

Bu paket qishloq xo'jaligi robotlari uchun interaktiv dala
rejalashtirish tizimini ta'minlaydi.

Modullar:
- environment_modeling: Muhit modellashtirish va to'siqlar
- coverage_planning: Dala qoplash yo'li rejalashtirish
"""

__version__ = "1.0.0"
__author__ = "Agricultural Robotics Team"

from .environment_modeling import EnvironmentMap, GridCell, ObstacleType, Obstacle
from .coverage_planning import FieldPolygon, CoveragePathPlanner, CoverageResult

__all__ = [
    'EnvironmentMap',
    'GridCell', 
    'ObstacleType',
    'Obstacle',
    'FieldPolygon',
    'CoveragePathPlanner',
    'CoverageResult'
]
