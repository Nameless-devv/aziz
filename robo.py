#!/usr/bin/env python3
# type: ignore
# pyright: reportGeneralTypeIssues=false
"""
Interaktiv Dala va To'siq Yaratish Dasturi
==========================================

Bu dastur orqali:
1. Ixtiyoriy shakldagi dalani yaratish mumkin
2. To'siqlarni interaktiv qo'shish mumkin
3. Robot yo'lini ko'rish mumkin (coverage path planning)

Foydalanish:
- Maydon yaratish: nuqtalarni birma-bir kiritish
- To'siq qo'shish: daraxt, tosh, bino va hokazo
- Yo'l rejalashtirish: boustrophedon yoki spiral
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from matplotlib.widgets import Button, RadioButtons, TextBox, Slider
from matplotlib.backend_bases import MouseButton
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import List, Tuple, Optional, Any
import sys
from pathlib import Path

# Src modullarini import qilish
sys.path.insert(0, str(Path(__file__).parent))

from src.environment_modeling import Obstacle, ObstacleType
from src.coverage_planning import FieldPolygon, CoveragePathPlanner, CoverageResult


class InteractiveFieldPlanner:
    """
    Interaktiv maydon va yo'l rejalashtiruvchi
    """
    
    def __init__(self):
        # Maydon va to'siqlar
        self.field_vertices: List[Tuple[float, float]] = []
        self.obstacles: List[dict] = []
        self.current_obstacle_vertices: List[Tuple[float, float]] = []
        
        # Planner
        self.planner: Optional[CoveragePathPlanner] = None
        self.coverage_result: Optional[CoverageResult] = None
        
        # Holat
        self.mode = "field"  # "field", "obstacle", "view", "start"
        self.current_obstacle_type = ObstacleType.TREE
        
        # Parametrlar
        self.working_width = 3.0  # metr
        self.overlap = 0.1
        self.obstacle_radius = 4.0  # To'siq radiusi (kattaroq)
        
        # Boshlang'ich nuqta
        self.start_point: Optional[Tuple[float, float]] = None
        self.start_marker: Any = None
        
        # Vizualizatsiya
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
        self.info_text: Any = None
        self.radius_text: Any = None
        
        # Callbacks
        self.field_polygon_patch: Any = None
        self.obstacle_patches: List[Any] = []
        self.path_line: Any = None
        self.temp_line: Any = None
    
    def setup_ui(self):
        """Interaktiv UI sozlash"""
        self.fig, self.ax = plt.subplots(figsize=(14, 10))  # type: ignore
        plt.subplots_adjust(left=0.05, right=0.75, top=0.95, bottom=0.05)
        
        # Asosiy maydon
        self.ax.set_xlim(-5, 105)
        self.ax.set_ylim(-5, 75)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.5)  # type: ignore
        self.ax.set_xlabel('X (metr)')  # type: ignore
        self.ax.set_ylabel('Y (metr)')  # type: ignore
        self.ax.set_title('🌾 Qishloq Xo\'jaligi Roboti - Maydon Yaratish', fontsize=14)  # type: ignore
        
        # Info panel
        info_ax = plt.axes((0.77, 0.6, 0.21, 0.35))  # type: ignore
        info_ax.axis('off')
        self.info_text = info_ax.text(
            0, 1, self._get_info_text(),
            transform=info_ax.transAxes,
            fontsize=10, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        # Rejim tugmalari
        mode_ax = plt.axes((0.77, 0.45, 0.21, 0.14))  # type: ignore
        self.mode_radio = RadioButtons(mode_ax, ['Maydon', 'To\'siq', 'Boshlash', 'Ko\'rish'])
        self.mode_radio.on_clicked(self._on_mode_change)  # type: ignore
        
        # To'siq turi
        obs_ax = plt.axes((0.77, 0.32, 0.21, 0.12))  # type: ignore
        obs_ax.set_title('To\'siq turi:', fontsize=9)
        self.obs_radio = RadioButtons(obs_ax, ['Daraxt', 'Tosh', 'Bino', 'Suv', 'Boshqa'])
        self.obs_radio.on_clicked(self._on_obstacle_type_change)  # type: ignore
        
        # To'siq hajmi slider
        slider_ax = plt.axes((0.77, 0.26, 0.21, 0.03))  # type: ignore
        self.radius_slider = Slider(
            slider_ax, 'Hajm:', 1.0, 10.0, 
            valinit=self.obstacle_radius,
            valstep=0.5
        )
        self.radius_slider.on_changed(self._on_radius_change)
        
        # Hajm ko'rsatkichi
        self.radius_label = plt.axes((0.77, 0.23, 0.21, 0.02))  # type: ignore
        self.radius_label.axis('off')
        self.radius_text = self.radius_label.text(
            0.5, 0.5, f'To\'siq radiusi: {self.obstacle_radius:.1f} m',
            ha='center', fontsize=9
        )
        
        # Amal tugmalari
        btn_clear = plt.axes((0.77, 0.17, 0.1, 0.04))  # type: ignore
        self.btn_clear = Button(btn_clear, 'Tozalash')
        self.btn_clear.on_clicked(self._on_clear)
        
        btn_plan = plt.axes((0.88, 0.17, 0.1, 0.04))  # type: ignore
        self.btn_plan = Button(btn_plan, 'Yo\'l')
        self.btn_plan.on_clicked(self._on_plan)
        
        btn_spiral = plt.axes((0.77, 0.12, 0.1, 0.04))  # type: ignore
        self.btn_spiral = Button(btn_spiral, 'Spiral')
        self.btn_spiral.on_clicked(self._on_spiral)
        
        btn_save = plt.axes((0.88, 0.12, 0.1, 0.04))  # type: ignore
        self.btn_save = Button(btn_save, 'Saqlash')
        self.btn_save.on_clicked(self._on_save)
        
        # Simulyatsiya tugmasi
        btn_sim_ax = plt.axes((0.77, 0.06, 0.21, 0.05))  # type: ignore
        self.btn_simulate = Button(btn_sim_ax, '🚜 SIMULYATSIYA', color='lightgreen', hovercolor='green')
        self.btn_simulate.on_clicked(self._on_simulate)
        
        # Parametrlar
        param_ax = plt.axes((0.77, 0.01, 0.21, 0.04))  # type: ignore
        param_ax.axis('off')
        param_ax.text(0, 0.5, f'Robot: {self.working_width}m | Overlap: {self.overlap*100:.0f}%', fontsize=8)
        
        # Mouse events
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)  # type: ignore
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)  # type: ignore
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)  # type: ignore
        
        # Legend
        self._update_legend()
    
    def _get_info_text(self) -> str:
        """Ma'lumot matnini yaratish"""
        info = "═══ Ma'lumot ═══\n\n"
        
        if self.mode == "field":
            info += "🔵 Maydon yaratish rejimi\n\n"
            info += "Chap klik: nuqta qo'shish\n"
            info += "Enter: maydonni yakunlash\n"
            info += f"Nuqtalar: {len(self.field_vertices)}\n"
        elif self.mode == "obstacle":
            info += "🔴 To'siq qo'shish rejimi\n\n"
            info += "Chap klik: to'siq markazi\n"
            info += f"To'siq radiusi: {self.obstacle_radius} m\n"
            info += f"To'siqlar: {len(self.obstacles)}\n"
        elif self.mode == "start":
            info += "🟢 Boshlash nuqtasi rejimi\n\n"
            info += "Chap klik: robot boshlanishi\n"
            if self.start_point:
                info += f"Nuqta: ({self.start_point[0]:.1f}, {self.start_point[1]:.1f})\n"
            else:
                info += "Nuqta: tanlanmagan\n"
        else:
            info += "👁️ Ko'rish rejimi\n\n"
            info += "Yo'lni ko'rish\n"
        
        if self.field_vertices:
            if len(self.field_vertices) >= 3:
                field = FieldPolygon(self.field_vertices)
                info += f"\n═══ Maydon ═══\n"
                info += f"Yuza: {field.get_area():.1f} m²\n"
        
        if self.coverage_result and self.coverage_result.success:
            info += f"\n═══ Yo'l ═══\n"
            info += f"Masofa: {self.coverage_result.total_distance:.1f} m\n"
            info += f"Qoplangan: {self.coverage_result.coverage_percentage:.1f}%\n"
            info += f"Qatorlar: {self.coverage_result.num_rows}\n"
        
        return info
    
    def _update_info(self):
        """Ma'lumotni yangilash"""
        if self.info_text:
            self.info_text.set_text(self._get_info_text())
        if self.fig:
            self.fig.canvas.draw_idle()  # type: ignore
    
    def _update_legend(self):
        """Legend yangilash"""
        legend_elements = [
            patches.Patch(facecolor='lightgreen', edgecolor='green', label='Maydon'),
            patches.Patch(facecolor='brown', edgecolor='black', label='Daraxt'),
            patches.Patch(facecolor='gray', edgecolor='black', label='Tosh'),
            Line2D([0], [0], color='blue', linewidth=2, label='Robot yo\'li'),
        ]
        if self.ax:
            self.ax.legend(handles=legend_elements, loc='upper left', fontsize=8)  # type: ignore
    
    def _on_mode_change(self, label: str):
        """Rejim o'zgartirish"""
        mode_map = {'Maydon': 'field', 'To\'siq': 'obstacle', 'Boshlash': 'start', 'Ko\'rish': 'view'}
        self.mode = mode_map.get(label, 'view')
        self._update_info()
    
    def _on_radius_change(self, val: float):
        """To'siq radiusini o'zgartirish"""
        self.obstacle_radius = val
        self.radius_text.set_text(f'To\'siq radiusi: {val:.1f} m')
        if self.fig:
            self.fig.canvas.draw_idle()  # type: ignore
    
    def _on_obstacle_type_change(self, label: str):
        """To'siq turini o'zgartirish"""
        type_map = {
            'Daraxt': ObstacleType.TREE,
            'Tosh': ObstacleType.ROCK,
            'Bino': ObstacleType.BUILDING,
            'Suv': ObstacleType.IRRIGATION,
            'Boshqa': ObstacleType.UNKNOWN
        }
        self.current_obstacle_type = type_map.get(label, ObstacleType.UNKNOWN)
    
    def _on_click(self, event):
        """Sichqoncha bosilishi"""
        if event.inaxes != self.ax:
            return
        
        x, y = event.xdata, event.ydata
        
        if self.mode == "field":
            if event.button == MouseButton.LEFT:
                self.field_vertices.append((x, y))
                self._draw_field_preview()
                self._update_info()
        
        elif self.mode == "obstacle":
            if event.button == MouseButton.LEFT:
                # Oddiy doira to'siq (kattaroq radius)
                self._add_obstacle_circle(x, y, radius=self.obstacle_radius)
            elif event.button == MouseButton.RIGHT:
                # Polygon to'siq boshlanishi
                self.current_obstacle_vertices.append((x, y))
                self._draw_obstacle_preview()
        
        elif self.mode == "start":
            if event.button == MouseButton.LEFT:
                # Boshlang'ich nuqtani tanlash
                self._set_start_point(x, y)
    
    def _on_motion(self, event):
        """Sichqoncha harakati"""
        if event.inaxes != self.ax:
            return
        
        if self.mode == "field" and len(self.field_vertices) > 0:
            # Preview chizish
            if self.temp_line:
                self.temp_line.remove()
            
            x, y = event.xdata, event.ydata
            xs = [v[0] for v in self.field_vertices] + [x]
            ys = [v[1] for v in self.field_vertices] + [y]
            
            self.temp_line, = self.ax.plot(xs, ys, 'g--', alpha=0.5)
            self.fig.canvas.draw_idle()
    
    def _on_key(self, event):
        """Klaviatura bosilishi"""
        if event.key == 'enter':
            if self.mode == "field" and len(self.field_vertices) >= 3:
                self._finalize_field()
            elif self.mode == "obstacle" and len(self.current_obstacle_vertices) >= 3:
                self._finalize_obstacle_polygon()
        
        elif event.key == 'escape':
            if self.mode == "field":
                self.field_vertices.clear()
            self.current_obstacle_vertices.clear()
            self._redraw()
        
        elif event.key == 'backspace':
            if self.mode == "field" and self.field_vertices:
                self.field_vertices.pop()
                self._draw_field_preview()
    
    def _add_obstacle_circle(self, x: float, y: float, radius: float = 2.0):
        """Doira to'siq qo'shish"""
        obstacle = {
            'type': self.current_obstacle_type,
            'position': (x, y),
            'size': (radius * 2, radius * 2),
            'shape': 'circle',
            'radius': radius
        }
        self.obstacles.append(obstacle)
        self._draw_obstacle(obstacle)
        self._update_info()
    
    def _finalize_field(self):
        """Maydonni yakunlash"""
        if self.temp_line:
            self.temp_line.remove()
            self.temp_line = None
        
        self._draw_field()
        self.mode = "obstacle"
        self.mode_radio.set_active(1)
        self._update_info()
    
    def _finalize_obstacle_polygon(self):
        """Polygon to'siqni yakunlash"""
        vertices = self.current_obstacle_vertices.copy()
        
        # Markaz va o'lcham hisoblash
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        obstacle = {
            'type': self.current_obstacle_type,
            'position': (cx, cy),
            'size': (width, height),
            'shape': 'polygon',
            'vertices': vertices
        }
        self.obstacles.append(obstacle)
        
        self.current_obstacle_vertices.clear()
        self._draw_obstacle(obstacle)
        self._update_info()
    
    def _draw_field_preview(self):
        """Maydon preview chizish"""
        self._redraw()
        
        if len(self.field_vertices) > 0:
            xs = [v[0] for v in self.field_vertices]
            ys = [v[1] for v in self.field_vertices]
            
            # Nuqtalar
            self.ax.scatter(xs, ys, c='green', s=50, zorder=5)
            
            # Chiziq
            if len(self.field_vertices) > 1:
                self.ax.plot(xs, ys, 'g-', linewidth=2)
    
    def _draw_field(self):
        """Maydonni chizish"""
        if len(self.field_vertices) < 3:
            return
        
        if self.field_polygon_patch:
            self.field_polygon_patch.remove()
        
        self.field_polygon_patch = patches.Polygon(
            self.field_vertices,
            facecolor='lightgreen',
            edgecolor='darkgreen',
            linewidth=2,
            alpha=0.5
        )
        self.ax.add_patch(self.field_polygon_patch)
        self.fig.canvas.draw_idle()
    
    def _draw_obstacle_preview(self):
        """To'siq preview"""
        self._redraw()
        
        if self.current_obstacle_vertices:
            xs = [v[0] for v in self.current_obstacle_vertices]
            ys = [v[1] for v in self.current_obstacle_vertices]
            self.ax.scatter(xs, ys, c='red', s=30, zorder=5)
            if len(self.current_obstacle_vertices) > 1:
                self.ax.plot(xs + [xs[0]], ys + [ys[0]], 'r--', alpha=0.5)
    
    def _set_start_point(self, x: float, y: float):
        """Boshlang'ich nuqtani belgilash"""
        self.start_point = (x, y)
        
        # Eski markerni o'chirish
        if self.start_marker:
            self.start_marker.remove()
        
        # Yangi marker chizish
        self.start_marker = self.ax.scatter(
            x, y, c='lime', s=300, marker='*', 
            edgecolors='darkgreen', linewidths=2, zorder=15,
            label='Boshlash nuqtasi'
        )
        
        # Matn qo'shish
        self.ax.annotate(
            'START', (x, y), 
            xytext=(x + 2, y + 2),
            fontsize=10, fontweight='bold', color='darkgreen',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8)
        )
        
        self._update_info()
        self.fig.canvas.draw_idle()
        print(f"✅ Boshlang'ich nuqta: ({x:.1f}, {y:.1f})")
    
    def _draw_obstacle(self, obstacle: dict):
        """To'siqni chizish"""
        color_map = {
            ObstacleType.TREE: 'darkgreen',
            ObstacleType.ROCK: 'dimgray',
            ObstacleType.BUILDING: 'saddlebrown',
            ObstacleType.IRRIGATION: 'royalblue',
            ObstacleType.UNKNOWN: 'darkviolet'
        }
        
        # Belgilar (marker)
        marker_map = {
            ObstacleType.TREE: '^',         # Uchburchak (daraxt)
            ObstacleType.ROCK: 's',         # Kvadrat (tosh)
            ObstacleType.BUILDING: 'p',     # Pentagon (bino)
            ObstacleType.IRRIGATION: 'o',   # Doira (suv)
            ObstacleType.UNKNOWN: 'X'       # X (noma'lum)
        }
        
        color = color_map.get(obstacle['type'], 'gray')
        marker = marker_map.get(obstacle['type'], 'o')
        
        if obstacle['shape'] == 'circle':
            # Doira to'siq - kattaroq va rangli
            circle = patches.Circle(
                obstacle['position'],
                obstacle['radius'],
                facecolor=color,
                edgecolor='black',
                linewidth=2,
                alpha=0.8
            )
            patch = self.ax.add_patch(circle)
            
            # Markazga marker qo'shish
            pos = obstacle['position']
            self.ax.scatter(pos[0], pos[1], c='white', s=100, 
                          marker=marker, edgecolors='black', linewidths=1, zorder=10)
        else:
            poly = patches.Polygon(
                obstacle['vertices'],
                facecolor=color,
                edgecolor='black',
                linewidth=2,
                alpha=0.8
            )
            patch = self.ax.add_patch(poly)
            
            # Markazga marker
            pos = obstacle['position']
            self.ax.scatter(pos[0], pos[1], c='white', s=80, 
                          marker=marker, edgecolors='black', linewidths=1, zorder=10)
        
        self.obstacle_patches.append(patch)
        self.fig.canvas.draw_idle()
    
    def _redraw(self):
        """Hammani qayta chizish"""
        # Eski patchlarni o'chirish
        for patch in self.obstacle_patches:
            patch.remove()
        self.obstacle_patches.clear()
        
        if self.path_line:
            self.path_line.remove()
            self.path_line = None
        
        # Maydonni chizish
        self._draw_field()
        
        # To'siqlarni chizish
        for obs in self.obstacles:
            self._draw_obstacle(obs)
        
        self.fig.canvas.draw_idle()
    
    def _on_clear(self, event):
        """Tozalash"""
        self.field_vertices.clear()
        self.obstacles.clear()
        self.current_obstacle_vertices.clear()
        self.coverage_result = None
        
        if self.field_polygon_patch:
            self.field_polygon_patch.remove()
            self.field_polygon_patch = None
        
        for patch in self.obstacle_patches:
            patch.remove()
        self.obstacle_patches.clear()
        
        if self.path_line:
            self.path_line.remove()
            self.path_line = None
        
        self.ax.clear()
        self.ax.set_xlim(-5, 105)
        self.ax.set_ylim(-5, 75)
        self.ax.set_aspect('equal')
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.set_xlabel('X (metr)')
        self.ax.set_ylabel('Y (metr)')
        self.ax.set_title('🌾 Qishloq Xo\'jaligi Roboti - Maydon Yaratish', fontsize=14)
        self._update_legend()
        self._update_info()
    
    def _on_plan(self, event):
        """Boustrophedon yo'l rejalashtirish"""
        self._plan_path(pattern='boustrophedon')
    
    def _on_spiral(self, event):
        """Spiral yo'l rejalashtirish"""
        self._plan_path(pattern='spiral')
    
    def _plan_path(self, pattern: str = 'boustrophedon'):
        """Yo'l rejalashtirish"""
        if len(self.field_vertices) < 3:
            print("Avval maydon yarating!")
            return
        
        # Planner yaratish
        field = FieldPolygon(self.field_vertices, name="Foydalanuvchi maydoni")
        self.planner = CoveragePathPlanner(
            field, 
            working_width=self.working_width,
            overlap=self.overlap
        )
        
        # To'siqlarni qo'shish
        for obs in self.obstacles:
            radius = obs.get('radius', max(obs['size']) / 2)
            obstacle = Obstacle(
                obstacle_id=len(self.planner.obstacles),
                obstacle_type=obs['type'],
                position=obs['position'],
                size=obs['size'],
                shape=obs['shape'],
                radius=radius
            )
            if obs['shape'] == 'polygon':
                obstacle.vertices = obs['vertices']
            self.planner.add_obstacle(obstacle)
        
        # Yo'l rejalashtirish
        if pattern == 'spiral':
            self.coverage_result = self.planner.plan_spiral()
        else:
            self.coverage_result = self.planner.plan_boustrophedon()
        
        # Yo'lni chizish
        self._draw_path()
        self._update_info()
    
    def _draw_path(self):
        """Yo'lni chizish"""
        if not self.coverage_result or not self.coverage_result.path:
            return
        
        if self.path_line:
            self.path_line.remove()
        
        path = self.coverage_result.path
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        
        self.path_line, = self.ax.plot(
            xs, ys, 'b-', linewidth=1.5, alpha=0.7, label='Robot yo\'li'
        )
        
        # Boshlang'ich nuqta
        if path:
            self.ax.scatter(path[0][0], path[0][1], c='green', s=100, 
                          marker='s', zorder=10, label='Boshlash')
            self.ax.scatter(path[-1][0], path[-1][1], c='red', s=100,
                          marker='*', zorder=10, label='Tugash')
        
        self.fig.canvas.draw_idle()
    
    def _on_save(self, event):
        """Natijalarni saqlash"""
        if self.coverage_result:
            import json
            
            data = {
                'field': self.field_vertices,
                'obstacles': [
                    {
                        'type': obs['type'].value,
                        'position': obs['position'],
                        'size': obs['size'],
                        'shape': obs['shape']
                    }
                    for obs in self.obstacles
                ],
                'path': self.coverage_result.path,
                'stats': {
                    'total_distance': self.coverage_result.total_distance,
                    'coverage_percentage': self.coverage_result.coverage_percentage,
                    'num_rows': self.coverage_result.num_rows
                }
            }
            
            with open('results/coverage_plan.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print("✅ Natijalar saqlandi: results/coverage_plan.json")
            print("\n🚜 Simulyatsiyani ishga tushirish uchun:")
            print("   python robot_simulation.py")
    
    def _on_simulate(self, event):
        """Simulyatsiyani ishga tushirish"""
        if not self.coverage_result or not self.coverage_result.path:
            print("❌ Avval yo'l rejalashtiring!")
            return
        
        # Avval saqlash
        self._on_save(event)
        
        # Boshlang'ich nuqtadan yo'lni qayta tartiblash
        path = self.coverage_result.path.copy()
        
        if self.start_point:
            # Eng yaqin nuqtani topish
            min_dist = float('inf')
            start_idx = 0
            for i, p in enumerate(path):
                dist = (p[0] - self.start_point[0])**2 + (p[1] - self.start_point[1])**2
                if dist < min_dist:
                    min_dist = dist
                    start_idx = i
            
            # Yo'lni qayta tartiblash
            path = path[start_idx:] + path[:start_idx]
            print(f"✅ Yo'l boshlang'ich nuqtadan ({self.start_point[0]:.1f}, {self.start_point[1]:.1f}) boshlanadi")
        
        print("\n🚜 Simulyatsiya boshlanmoqda...")
        
        # Simulyatsiya oynasini ochish
        self._run_simulation(path)
    
    def _run_simulation(self, path: List[Tuple[float, float]]):
        """Robot simulyatsiyasi"""
        from matplotlib.animation import FuncAnimation
        import matplotlib.transforms as transforms
        
        # Yangi oyna
        sim_fig, sim_ax = plt.subplots(figsize=(12, 9))
        sim_ax.set_aspect('equal')
        
        # Chegaralar
        xs = [v[0] for v in self.field_vertices]
        ys = [v[1] for v in self.field_vertices]
        margin = 5
        sim_ax.set_xlim(min(xs) - margin, max(xs) + margin)
        sim_ax.set_ylim(min(ys) - margin, max(ys) + margin)
        sim_ax.grid(True, linestyle='--', alpha=0.3)
        sim_ax.set_xlabel('X (metr)')
        sim_ax.set_ylabel('Y (metr)')
        sim_ax.set_title('🚜 Robot Simulyatsiyasi - Dori Sepish', fontsize=14, fontweight='bold')
        
        # Maydon
        field_patch = patches.Polygon(
            self.field_vertices,
            facecolor='lightgreen',
            edgecolor='darkgreen',
            linewidth=2,
            alpha=0.5
        )
        sim_ax.add_patch(field_patch)
        
        # To'siqlar
        for obs in self.obstacles:
            color_map = {
                ObstacleType.TREE: 'darkgreen',
                ObstacleType.ROCK: 'dimgray',
                ObstacleType.BUILDING: 'saddlebrown',
                ObstacleType.IRRIGATION: 'royalblue',
                ObstacleType.UNKNOWN: 'darkviolet'
            }
            color = color_map.get(obs['type'], 'gray')
            
            if obs['shape'] == 'circle':
                circle = patches.Circle(
                    obs['position'],
                    obs.get('radius', 3),
                    facecolor=color,
                    edgecolor='black',
                    linewidth=2,
                    alpha=0.8
                )
                sim_ax.add_patch(circle)
        
        # Yo'l (xira)
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        sim_ax.plot(path_x, path_y, 'b--', alpha=0.2, linewidth=1)
        
        # Sepilgan yo'l
        spray_line, = sim_ax.plot([], [], 'b-', linewidth=self.working_width * 3, 
                                   alpha=0.4, solid_capstyle='round')
        
        # Robot
        robot_size = self.working_width
        robot = patches.FancyBboxPatch(
            (-robot_size * 0.75, -robot_size / 2), 
            robot_size * 1.5, robot_size,
            boxstyle="round,pad=0.1",
            facecolor='red',
            edgecolor='darkred',
            linewidth=2
        )
        sim_ax.add_patch(robot)
        
        # Ma'lumot paneli
        info_text = sim_ax.text(
            0.02, 0.98, '', transform=sim_ax.transAxes,
            fontsize=11, verticalalignment='top',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        
        # Animatsiya holati
        current_idx = [0]
        sprayed = []
        distance = [0.0]
        
        def animate(frame):
            steps = 3
            for _ in range(steps):
                if current_idx[0] >= len(path) - 1:
                    # Animatsiya tugadi - statistika ko'rsatish
                    on_animation_complete()
                    return []
                
                current = path[current_idx[0]]
                next_pt = path[current_idx[0] + 1]
                
                sprayed.append(current)
                
                dx = next_pt[0] - current[0]
                dy = next_pt[1] - current[1]
                distance[0] += np.sqrt(dx**2 + dy**2)
                
                current_idx[0] += 1
            
            # Robot pozitsiyasi
            if current_idx[0] < len(path):
                curr = path[current_idx[0]]
                if current_idx[0] < len(path) - 1:
                    nxt = path[current_idx[0] + 1]
                    theta = np.arctan2(nxt[1] - curr[1], nxt[0] - curr[0])
                else:
                    theta = 0
                
                t = transforms.Affine2D().rotate(theta).translate(curr[0], curr[1]) + sim_ax.transData
                robot.set_transform(t)
            
            # Sepilgan yo'l
            if sprayed:
                spray_line.set_data([p[0] for p in sprayed], [p[1] for p in sprayed])
            
            # Ma'lumot
            progress = (current_idx[0] / len(path)) * 100
            info_text.set_text(
                f"═══ Robot Holati ═══\n"
                f"Pozitsiya: ({path[current_idx[0]][0]:.1f}, {path[current_idx[0]][1]:.1f})\n"
                f"Bosib o'tilgan: {distance[0]:.1f} m\n"
                f"Progress: {progress:.1f}%"
            )
            
            return [robot, spray_line, info_text]
        
        def on_animation_complete():
            """Animatsiya tugagach statistika ko'rsatish"""
            # Maydon yuzasi
            field = FieldPolygon(self.field_vertices)
            area = field.get_area()
            
            # Statistika paneli
            stats_text = (
                f"═══ SIMULYATSIYA TUGADI ═══\n\n"
                f"📊 YAKUNIY STATISTIKA:\n\n"
                f"🌾 Maydon yuzasi: {area:.1f} m²\n"
                f"🚀 Bosib o'tilgan masofa: {distance[0]:.1f} m\n"
                f"📈 Qoplash foizi: {self.coverage_result.coverage_percentage:.1f}%\n"
                f"🔄 Qatorlar soni: {self.coverage_result.num_rows}\n"
                f"⏱️ Yo'l nuqtalari: {len(path)}\n"
                f"🤖 Robot kengligi: {self.working_width} m\n"
                f"📐 Overlap: {self.overlap*100:.0f}%\n"
                f"🌳 To'siqlar soni: {len(self.obstacles)}\n\n"
                f"✅ Simulyatsiya muvaffaqiyatli tugadi!"
            )
            
            info_text.set_text(stats_text)
            info_text.set_bbox(dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
            
            # Sarlavha o'zgartirish
            sim_ax.set_title('🚜 Robot Simulyatsiyasi - YAKUNLANDI', fontsize=14, fontweight='bold', color='green')
            
            # Tugash nuqtasini belgilash
            if path:
                sim_ax.scatter(path[-1][0], path[-1][1], c='red', s=200, 
                              marker='*', zorder=15, linewidths=2, edgecolors='darkred')
                sim_ax.annotate('TUGASH', (path[-1][0], path[-1][1]), 
                               xytext=(path[-1][0] + 3, path[-1][1] + 3),
                               fontsize=12, fontweight='bold', color='red',
                               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
            
            sim_fig.canvas.draw()
            print("✅ Simulyatsiya tugadi! Oyna ochiq qolmoqda.")
        
        frames = len(path) // 3 + 1
        anim = FuncAnimation(sim_fig, animate, frames=frames, interval=30, blit=True, repeat=False)
        
        plt.show()
    
    def run(self):
        """Dasturni ishga tushirish"""
        self.setup_ui()
        
        print("\n" + "="*50)
        print("🌾 Qishloq Xo'jaligi Roboti - Interaktiv Planner")
        print("="*50)
        print("\n📋 Ko'rsatmalar:")
        print("1. 'Maydon' rejimida dala chegaralarini chizing")
        print("   - Chap klik: nuqta qo'shish")
        print("   - Enter: maydonni yakunlash")
        print("2. 'To'siq' rejimida to'siqlarni qo'shing")
        print("   - Chap klik: doira to'siq")
        print("3. 'Yo'l' tugmasini bosib yo'lni ko'ring")
        print("\n⌨️ Klaviatura:")
        print("   Enter: yakunlash")
        print("   Escape: bekor qilish")
        print("   Backspace: oxirgi nuqtani o'chirish")
        print("="*50 + "\n")
        
        plt.show()


def main():
    """Asosiy funksiya"""
    planner = InteractiveFieldPlanner()
    planner.run()


if __name__ == "__main__":
    main()
