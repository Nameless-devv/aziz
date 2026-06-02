"""
Coverage Path Planning Module
==============================

Robot butun maydonni qoplashi uchun yo'l rejalashtirish.
Qishloq xo'jaligida: dori sepish, o'rim-yig'im, sugorish uchun.

Vazifalar:
- Ixtiyoriy shakldagi maydonni qo'llab-quvvatlash
- Butun maydonni qoplash (coverage)
- To'siqlardan aylanib o'tish
- Parallel qator (boustrophedon) yo'l yaratish
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
import time

from .environment_modeling import EnvironmentMap, Obstacle, ObstacleType


class CoveragePattern(Enum):
    """Qoplash naqshlari"""
    BOUSTROPHEDON = "boustrophedon"  # Ilon yo'li (parallel qatorlar)
    SPIRAL = "spiral"  # Spiral
    ZIGZAG = "zigzag"  # Zigzag


@dataclass
class FieldPolygon:
    """
    Ixtiyoriy shakldagi maydon
    
    Attributes:
        vertices: Maydon cho'qqilari (soat yo'nalishida)
        name: Maydon nomi
    """
    vertices: List[Tuple[float, float]]
    name: str = "Maydon"
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Maydon chegaralarini olish (min_x, min_y, max_x, max_y)"""
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        return min(xs), min(ys), max(xs), max(ys)
    
    def get_area(self) -> float:
        """Maydon yuzasini hisoblash (Shoelace formula)"""
        n = len(self.vertices)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.vertices[i][0] * self.vertices[j][1]
            area -= self.vertices[j][0] * self.vertices[i][1]
        return abs(area) / 2.0
    
    def contains_point(self, x: float, y: float) -> bool:
        """Nuqta maydon ichida yoki yo'qligini tekshirish (Ray casting)"""
        n = len(self.vertices)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        
        return inside
    
    def get_edge_at_y(self, y: float) -> List[float]:
        """Berilgan y da maydon kesishish nuqtalarini topish"""
        intersections: List[float] = []
        n = len(self.vertices)
        
        for i in range(n):
            j = (i + 1) % n
            yi, yj = self.vertices[i][1], self.vertices[j][1]
            xi, xj = self.vertices[i][0], self.vertices[j][0]
            
            # Y qator bu qirra bilan kesishadimi?
            if (yi <= y < yj) or (yj <= y < yi):
                if yj != yi:
                    x = xi + (y - yi) * (xj - xi) / (yj - yi)
                    intersections.append(x)
        
        return sorted(intersections)


@dataclass
class CoverageResult:
    """
    Coverage planning natijasi
    
    Attributes:
        path: Yo'l nuqtalari
        coverage_percentage: Qoplangan maydon foizi
        total_distance: Umumiy masofa
        num_rows: Qatorlar soni
        computation_time: Hisoblash vaqti
    """
    path: List[Tuple[float, float]] = field(default_factory=list)
    coverage_percentage: float = 0.0
    total_distance: float = 0.0
    num_rows: int = 0
    computation_time: float = 0.0
    success: bool = False


class CoveragePathPlanner:
    """
    Coverage Path Planner
    
    Butun maydonni qoplash uchun yo'l rejalashtiradi.
    
    Attributes:
        field_polygon: Maydon shakli
        obstacles: To'siqlar ro'yxati
        working_width: Robot ish kengligi (metr)
        overlap: Qatorlar orasidagi overlap (0-1)
    """
    
    def __init__(self, field_polygon: FieldPolygon, 
                 working_width: float = 2.0,
                 overlap: float = 0.1):
        """
        Coverage planner yaratish
        
        Args:
            field_polygon: Maydon shakli
            working_width: Robot ish kengligi
            overlap: Qatorlar overlap foizi
        """
        self.field_polygon = field_polygon
        self.obstacles: List[Obstacle] = []
        self.working_width = working_width
        self.overlap = overlap
        
        # Effektiv qator oralig'i
        self.row_spacing = working_width * (1 - overlap)
        
        # To'siqlar xaritasi
        self._obstacle_grid: Optional[np.ndarray] = None
        self._grid_resolution = 0.1  # metr
    
    def add_obstacle(self, obstacle: Obstacle):
        """To'siq qo'shish"""
        self.obstacles.append(obstacle)
        self._update_obstacle_grid()
    
    def add_obstacle_polygon(self, vertices: List[Tuple[float, float]], 
                             obstacle_type: ObstacleType = ObstacleType.UNKNOWN):
        """Polygon shaklidagi to'siq qo'shish"""
        # Polygon markazini topish
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        
        # O'lchamni hisoblash
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        obstacle = Obstacle(
            obstacle_id=len(self.obstacles),
            obstacle_type=obstacle_type,
            position=(cx, cy),
            size=(width, height),
            vertices=vertices
        )
        self.add_obstacle(obstacle)
        return obstacle
    
    def clear_obstacles(self):
        """Barcha to'siqlarni o'chirish"""
        self.obstacles.clear()
        self._obstacle_grid = None
    
    def _update_obstacle_grid(self):
        """To'siqlar grid ni yangilash"""
        bounds = self.field_polygon.get_bounds()
        min_x, min_y, max_x, max_y = bounds
        
        grid_width = int((max_x - min_x) / self._grid_resolution) + 1
        grid_height = int((max_y - min_y) / self._grid_resolution) + 1
        
        self._obstacle_grid = np.zeros((grid_height, grid_width), dtype=bool)
        
        # Xavfsizlik masofa (robot radiusi)
        safety_margin = self.working_width / 2 + 0.5
        
        for obstacle in self.obstacles:
            # To'siq yuzasini grid ga belgilash
            ox, oy = obstacle.position
            w, h = obstacle.size
            
            # Doira radiusi (agar mavjud bo'lsa)
            radius = getattr(obstacle, 'radius', max(w, h) / 2)
            
            for gy in range(grid_height):
                for gx in range(grid_width):
                    px = min_x + gx * self._grid_resolution
                    py = min_y + gy * self._grid_resolution
                    
                    # To'siq ichidami?
                    if hasattr(obstacle, 'vertices') and obstacle.vertices:
                        # Polygon to'siq
                        if self._point_in_polygon(px, py, obstacle.vertices):
                            self._obstacle_grid[gy, gx] = True
                        # Polygon atrofida xavfsizlik zonasi
                        elif self._point_near_polygon(px, py, obstacle.vertices, safety_margin):
                            self._obstacle_grid[gy, gx] = True
                    else:
                        # Doira to'siq - radius + xavfsizlik masofa
                        dist = np.sqrt((px - ox)**2 + (py - oy)**2)
                        if dist <= radius + safety_margin:
                            self._obstacle_grid[gy, gx] = True
    
    def _point_near_polygon(self, x: float, y: float, 
                            vertices: List[Tuple[float, float]], 
                            margin: float) -> bool:
        """Nuqta polygon atrofida (margin ichida)mi?"""
        # Har bir polygon qirrasiga masofa tekshirish
        n = len(vertices)
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            
            # Nuqtadan qirraga masofa
            dist = self._point_to_segment_distance(x, y, x1, y1, x2, y2)
            if dist <= margin:
                return True
        return False
    
    def _point_to_segment_distance(self, px: float, py: float,
                                    x1: float, y1: float,
                                    x2: float, y2: float) -> float:
        """Nuqtadan segment (qirra)ga masofa"""
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return np.sqrt((px - x1)**2 + (py - y1)**2)
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return np.sqrt((px - closest_x)**2 + (py - closest_y)**2)
    
    def _point_in_polygon(self, x: float, y: float, 
                          vertices: List[Tuple[float, float]]) -> bool:
        """Nuqta polygon ichidami?"""
        n = len(vertices)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        return inside
    
    def _is_point_in_obstacle(self, x: float, y: float) -> bool:
        """Nuqta to'siq ichidami?"""
        if self._obstacle_grid is None:
            return False
        
        bounds = self.field_polygon.get_bounds()
        min_x, min_y, _, _ = bounds
        
        gx = int((x - min_x) / self._grid_resolution)
        gy = int((y - min_y) / self._grid_resolution)
        
        if 0 <= gy < self._obstacle_grid.shape[0] and 0 <= gx < self._obstacle_grid.shape[1]:
            return self._obstacle_grid[gy, gx]
        return False
    
    def plan_boustrophedon(self, start_corner: str = "bottom_left",
                           direction: str = "horizontal") -> CoverageResult:
        """
        Boustrophedon (ilon yo'li) naqshida yo'l rejalashtirish
        
        Args:
            start_corner: Boshlash burchagi ("bottom_left", "top_left", etc.)
            direction: Asosiy yo'nalish ("horizontal" yoki "vertical")
            
        Returns:
            CoverageResult
        """
        start_time = time.time()
        result = CoverageResult()
        
        bounds = self.field_polygon.get_bounds()
        min_x, min_y, max_x, max_y = bounds
        
        path: List[Tuple[float, float]] = []
        
        if direction == "horizontal":
            # Gorizontal qatorlar (pastdan yuqoriga)
            y = min_y + self.row_spacing / 2
            row_num = 0
            going_right = start_corner in ["bottom_left", "top_left"]
            
            if "top" in start_corner:
                y = max_y - self.row_spacing / 2
                self.row_spacing = -self.row_spacing
            
            while (self.row_spacing > 0 and y <= max_y) or \
                  (self.row_spacing < 0 and y >= min_y):
                
                # Bu y da maydon kesishish nuqtalarini topish
                intersections = self.field_polygon.get_edge_at_y(y)
                
                if len(intersections) >= 2:
                    # Juft kesishishlar orasida harakat
                    for i in range(0, len(intersections) - 1, 2):
                        x_start = intersections[i] + 0.2
                        x_end = intersections[i + 1] - 0.2
                        
                        if not going_right:
                            x_start, x_end = x_end, x_start
                        
                        # To'siqlarni tekshirish va aylanib o'tish
                        row_path = self._generate_row_with_obstacles(
                            x_start, x_end, y, going_right
                        )
                        path.extend(row_path)
                    
                    row_num += 1
                    going_right = not going_right
                
                y += abs(self.row_spacing) if self.row_spacing > 0 else -abs(self.row_spacing)
            
            # Reset row_spacing
            self.row_spacing = abs(self.row_spacing)
        
        else:  # vertical
            # Vertikal qatorlar (chapdan o'ngga)
            x = min_x + self.row_spacing / 2
            row_num = 0
            going_up = start_corner in ["bottom_left", "bottom_right"]
            
            while x <= max_x:
                # Vertikal qator
                y_points = []
                for y in np.arange(min_y, max_y, self._grid_resolution):
                    if self.field_polygon.contains_point(x, y):
                        y_points.append(y)
                
                if y_points:
                    y_start = min(y_points) + 0.2
                    y_end = max(y_points) - 0.2
                    
                    if not going_up:
                        y_start, y_end = y_end, y_start
                    
                    row_path = self._generate_vertical_row_with_obstacles(
                        x, y_start, y_end, going_up
                    )
                    path.extend(row_path)
                    
                    row_num += 1
                    going_up = not going_up
                
                x += self.row_spacing
        
        # Natijalarni hisoblash
        result.path = path
        result.num_rows = row_num
        result.total_distance = self._calculate_path_length(path)
        result.coverage_percentage = self._calculate_coverage(path)
        result.computation_time = time.time() - start_time
        result.success = len(path) > 0
        
        return result
    
    def _generate_row_with_obstacles(self, x_start: float, x_end: float, 
                                      y: float, going_right: bool) -> List[Tuple[float, float]]:
        """Gorizontal qator yaratish, to'siqlardan aylanib o'tish"""
        path = []
        
        step = self._grid_resolution if going_right else -self._grid_resolution
        x = x_start
        in_obstacle = False
        obstacle_start_x = None
        
        while (going_right and x <= x_end) or (not going_right and x >= x_end):
            if self.field_polygon.contains_point(x, y):
                is_in_obs = self._is_point_in_obstacle(x, y)
                
                if not is_in_obs:
                    if in_obstacle and obstacle_start_x is not None:
                        # To'siqdan chiqdik - aylanib o'tish yo'lini qo'shish
                        bypass = self._find_obstacle_bypass_path(
                            obstacle_start_x, x, y, going_right
                        )
                        if bypass:
                            path.extend(bypass)
                        in_obstacle = False
                        obstacle_start_x = None
                    else:
                        path.append((x, y))
                else:
                    if not in_obstacle:
                        # To'siqga kirdik
                        in_obstacle = True
                        obstacle_start_x = x - step  # Oldingi nuqta
            x += step
        
        return path
    
    def _find_obstacle_bypass_path(self, x_start: float, x_end: float, 
                                    y: float, going_right: bool) -> List[Tuple[float, float]]:
        """To'siqni aylanib o'tish - yuqoridan yoki pastdan"""
        
        # Yuqoridan aylanish
        up_path = self._try_bypass_direction(x_start, x_end, y, going_right, direction=1)
        
        # Pastdan aylanish
        down_path = self._try_bypass_direction(x_start, x_end, y, going_right, direction=-1)
        
        # Qisqa yo'lni tanlash
        if up_path and down_path:
            up_len = self._calculate_path_length(up_path)
            down_len = self._calculate_path_length(down_path)
            return up_path if up_len <= down_len else down_path
        elif up_path:
            return up_path
        elif down_path:
            return down_path
        else:
            return []
    
    def _try_bypass_direction(self, x_start: float, x_end: float, y: float, 
                               going_right: bool, direction: int) -> List[Tuple[float, float]]:
        """Bitta yo'nalishda aylanib o'tishni sinash - FAQAT maydon ichida"""
        path = []
        
        # To'siqdan qochish uchun y ga siljish
        safe_y = y
        max_attempts = 20
        
        for i in range(1, max_attempts):
            test_y = y + direction * i * self.row_spacing
            
            # Har ikkala uchida ham maydon ichida bo'lishi kerak
            if not self.field_polygon.contains_point(x_start, test_y) or \
               not self.field_polygon.contains_point(x_end, test_y):
                break
            
            # Butun yo'l bo'ylab to'siq yo'qligini va maydon ichida ekanligini tekshirish
            path_clear = True
            step = self._grid_resolution if going_right else -self._grid_resolution
            test_x = x_start
            
            while (going_right and test_x <= x_end) or (not going_right and test_x >= x_end):
                if not self.field_polygon.contains_point(test_x, test_y) or \
                   self._is_point_in_obstacle(test_x, test_y):
                    path_clear = False
                    break
                test_x += step
            
            if path_clear:
                safe_y = test_y
                break
        
        if safe_y == y:
            return []  # Yo'l topilmadi
        
        # Yo'lni yasash: yuqoriga -> gorizontal -> pastga
        # 1. Yuqoriga chiqish - faqat maydon ichida
        step_y = self._grid_resolution * direction
        curr_y = y
        while (direction > 0 and curr_y < safe_y) or (direction < 0 and curr_y > safe_y):
            if self.field_polygon.contains_point(x_start, curr_y) and \
               not self._is_point_in_obstacle(x_start, curr_y):
                path.append((x_start, curr_y))
            else:
                # Maydon tashqarisiga chiqqanda to'xtatish
                break
            curr_y += step_y
        
        # 2. Gorizontal harakat - faqat maydon ichida
        step_x = self._grid_resolution if going_right else -self._grid_resolution
        curr_x = x_start
        while (going_right and curr_x <= x_end) or (not going_right and curr_x >= x_end):
            if self.field_polygon.contains_point(curr_x, safe_y) and \
               not self._is_point_in_obstacle(curr_x, safe_y):
                path.append((curr_x, safe_y))
            curr_x += step_x
        
        # 3. Pastga tushish - faqat maydon ichida
        curr_y = safe_y
        while (direction > 0 and curr_y > y) or (direction < 0 and curr_y < y):
            curr_y -= step_y
            if self.field_polygon.contains_point(x_end, curr_y) and \
               not self._is_point_in_obstacle(x_end, curr_y):
                path.append((x_end, curr_y))
            else:
                break
        
        return path
    
    def _generate_vertical_row_with_obstacles(self, x: float, y_start: float,
                                               y_end: float, going_up: bool) -> List[Tuple[float, float]]:
        """Vertikal qator yaratish"""
        path = []
        
        step = self._grid_resolution if going_up else -self._grid_resolution
        y = y_start
        
        while (going_up and y <= y_end) or (not going_up and y >= y_end):
            if self.field_polygon.contains_point(x, y):
                if not self._is_point_in_obstacle(x, y):
                    path.append((x, y))
            y += step
        
        return path
    
    def _find_obstacle_bypass(self, x: float, y: float, 
                               going_right: bool) -> List[Tuple[float, float]]:
        """To'siqdan aylanib o'tish yo'lini topish - yaxshilangan algoritm"""
        bypass = []
        
        # To'siq chegaralarini topish
        obstacle_left = x
        obstacle_right = x
        
        # To'siq chegarasini chap va o'ngga kengaytirish
        step = self._grid_resolution
        
        # O'ng chegarani topish
        test_x = x
        while test_x <= self.field_polygon.get_bounds()[2]:
            if not self._is_point_in_obstacle(test_x, y):
                obstacle_right = test_x
                break
            test_x += step
        
        # Chap chegarani topish
        test_x = x
        while test_x >= self.field_polygon.get_bounds()[0]:
            if not self._is_point_in_obstacle(test_x, y):
                obstacle_left = test_x
                break
            test_x -= step
        
        # Yuqoriga yoki pastga aylanib o'tish
        # Eng qisqa yo'lni tanlash
        for direction in [1, -1]:  # 1 = yuqori, -1 = past
            found_path = []
            test_y = y + direction * self.row_spacing
            
            # To'siqdan yuqori/past bo'lgunga qadar harakatlanish
            safe_y = None
            for _ in range(10):  # Maksimum 10 qadam
                if not self._is_point_in_obstacle(x, test_y) and \
                   self.field_polygon.contains_point(x, test_y):
                    safe_y = test_y
                    break
                test_y += direction * self.row_spacing / 2
            
            if safe_y is not None:
                # Yuqoriga/pastga chiqish
                found_path.append((x, safe_y))
                
                # To'siq ustidan/ostidan o'tish
                if going_right:
                    # O'ngga harakatlanish
                    for bx in np.arange(x, obstacle_right + step, step):
                        if self.field_polygon.contains_point(bx, safe_y) and \
                           not self._is_point_in_obstacle(bx, safe_y):
                            found_path.append((bx, safe_y))
                else:
                    # Chapga harakatlanish
                    for bx in np.arange(x, obstacle_left - step, -step):
                        if self.field_polygon.contains_point(bx, safe_y) and \
                           not self._is_point_in_obstacle(bx, safe_y):
                            found_path.append((bx, safe_y))
                
                # Qaytib tushish
                found_path.append((found_path[-1][0], y))
                
                if found_path:
                    bypass = found_path
                    break
        
        return bypass
    
    def _calculate_path_length(self, path: List[Tuple[float, float]]) -> float:
        """Yo'l uzunligini hisoblash"""
        if len(path) < 2:
            return 0.0
        
        length = 0.0
        for i in range(len(path) - 1):
            dx = path[i+1][0] - path[i][0]
            dy = path[i+1][1] - path[i][1]
            length += np.sqrt(dx**2 + dy**2)
        
        return length
    
    def _calculate_coverage(self, path: List[Tuple[float, float]]) -> float:
        """Qoplangan maydon foizini hisoblash"""
        if not path:
            return 0.0
        
        field_area = self.field_polygon.get_area()
        
        # Obstacle maydonini ayirish
        obstacle_area = sum(obs.size[0] * obs.size[1] for obs in self.obstacles)
        effective_area = field_area - obstacle_area
        
        # Qoplangan maydon (yo'l uzunligi * ish kengligi)
        covered_area = self._calculate_path_length(path) * self.working_width
        
        return min(100.0, (covered_area / effective_area) * 100) if effective_area > 0 else 0.0
    
    def plan_spiral(self, inward: bool = True) -> CoverageResult:
        """
        Spiral naqshida yo'l rejalashtirish - to'siqlarni aylanib o'tadi
        
        Args:
            inward: Ichkariga spiral (True) yoki tashqariga (False)
            
        Returns:
            CoverageResult
        """
        start_time = time.time()
        result = CoverageResult()
        
        bounds = self.field_polygon.get_bounds()
        min_x, min_y, max_x, max_y = bounds
        
        path: List[Tuple[float, float]] = []
        
        # Spiral parametrlari
        offset = 0.0
        max_offset = min(max_x - min_x, max_y - min_y) / 2
        row_num = 0
        
        while offset < max_offset:
            # Hozirgi offset dagi to'rtburchak
            x1 = min_x + offset + 0.2
            y1 = min_y + offset + 0.2
            x2 = max_x - offset - 0.2
            y2 = max_y - offset - 0.2
            
            if x2 <= x1 or y2 <= y1:
                break
            
            # To'rtburchak perimetrini yurish - to'siqlarni aylanib
            # Pastki qirra
            row_path = self._generate_spiral_edge(x1, x2, y1, y1, 'horizontal', True)
            if row_path:
                path.extend(self._connect_path_avoiding_obstacles(path, row_path))
            
            # O'ng qirra
            row_path = self._generate_spiral_edge(x2, x2, y1, y2, 'vertical', True)
            if row_path:
                path.extend(self._connect_path_avoiding_obstacles(path, row_path))
            
            # Yuqori qirra (teskari)
            row_path = self._generate_spiral_edge(x2, x1, y2, y2, 'horizontal', False)
            if row_path:
                path.extend(self._connect_path_avoiding_obstacles(path, row_path))
            
            # Chap qirra (teskari)
            row_path = self._generate_spiral_edge(x1, x1, y2, y1 + self.row_spacing, 'vertical', False)
            if row_path:
                path.extend(self._connect_path_avoiding_obstacles(path, row_path))
            
            offset += self.row_spacing
            row_num += 1
        
        # Agar tashqariga spiral bo'lsa, yo'lni teskari qilish
        if not inward:
            path = path[::-1]
        
        result.path = path
        result.num_rows = row_num
        result.total_distance = self._calculate_path_length(path)
        result.coverage_percentage = self._calculate_coverage(path)
        result.computation_time = time.time() - start_time
        result.success = len(path) > 0
        
        return result
    
    def _generate_spiral_edge(self, x1: float, x2: float, y1: float, y2: float,
                               direction: str, forward: bool) -> List[Tuple[float, float]]:
        """Spiral qirrasi - to'siqlarni aylanib o'tish"""
        path = []
        
        if direction == 'horizontal':
            step = self._grid_resolution if forward else -self._grid_resolution
            x = x1
            y = y1
            
            in_obstacle = False
            obstacle_start = None
            
            while (forward and x <= x2) or (not forward and x >= x2):
                if self.field_polygon.contains_point(x, y):
                    if self._is_point_in_obstacle(x, y):
                        if not in_obstacle:
                            in_obstacle = True
                            obstacle_start = x - step
                    else:
                        if in_obstacle and obstacle_start is not None:
                            # To'siqdan chiqdik - aylanib o'tish
                            bypass = self._bypass_obstacle_on_edge(
                                obstacle_start, x, y, y, 'horizontal', forward
                            )
                            path.extend(bypass)
                            in_obstacle = False
                            obstacle_start = None
                        else:
                            path.append((x, y))
                x += step
                
        else:  # vertical
            step = self._grid_resolution if forward else -self._grid_resolution
            x = x1
            y = y1
            
            in_obstacle = False
            obstacle_start = None
            
            while (forward and y <= y2) or (not forward and y >= y2):
                if self.field_polygon.contains_point(x, y):
                    if self._is_point_in_obstacle(x, y):
                        if not in_obstacle:
                            in_obstacle = True
                            obstacle_start = y - step
                    else:
                        if in_obstacle and obstacle_start is not None:
                            bypass = self._bypass_obstacle_on_edge(
                                x, x, obstacle_start, y, 'vertical', forward
                            )
                            path.extend(bypass)
                            in_obstacle = False
                            obstacle_start = None
                        else:
                            path.append((x, y))
                y += step
        
        return path
    
    def _bypass_obstacle_on_edge(self, x1: float, x2: float, y1: float, y2: float,
                                  direction: str, forward: bool) -> List[Tuple[float, float]]:
        """To'siqni spiral qirrasida aylanib o'tish - FAQAT maydon ichida"""
        path = []
        
        if direction == 'horizontal':
            y = y1
            # Yuqoriga yoki pastga aylanish
            for dy_dir in [1, -1]:
                safe_y = None
                for i in range(1, 15):
                    test_y = y + dy_dir * i * self.row_spacing
                    
                    # Har ikkala uchida maydon ichida bo'lishi kerak
                    if not self.field_polygon.contains_point(x1, test_y) or \
                       not self.field_polygon.contains_point(x2, test_y):
                        break
                    
                    # Butun yo'l bo'ylab tekshirish - maydon ichida va to'siqsiz
                    clear = True
                    step = self._grid_resolution if forward else -self._grid_resolution
                    test_x = x1
                    while (forward and test_x <= x2) or (not forward and test_x >= x2):
                        if not self.field_polygon.contains_point(test_x, test_y) or \
                           self._is_point_in_obstacle(test_x, test_y):
                            clear = False
                            break
                        test_x += step
                    
                    if clear:
                        safe_y = test_y
                        break
                
                if safe_y is not None:
                    # Aylanib o'tish yo'lini yaratish - faqat maydon ichida
                    if self.field_polygon.contains_point(x1, safe_y):
                        path.append((x1, safe_y))
                    step = self._grid_resolution if forward else -self._grid_resolution
                    x = x1 + step
                    while (forward and x < x2) or (not forward and x > x2):
                        if self.field_polygon.contains_point(x, safe_y):
                            path.append((x, safe_y))
                        x += step
                    if self.field_polygon.contains_point(x2, safe_y):
                        path.append((x2, safe_y))
                    if self.field_polygon.contains_point(x2, y):
                        path.append((x2, y))
                    break
        else:
            x = x1
            for dx_dir in [1, -1]:
                safe_x = None
                for i in range(1, 15):
                    test_x = x + dx_dir * i * self.row_spacing
                    
                    # Har ikkala uchida maydon ichida bo'lishi kerak
                    if not self.field_polygon.contains_point(test_x, y1) or \
                       not self.field_polygon.contains_point(test_x, y2):
                        break
                    
                    clear = True
                    step = self._grid_resolution if forward else -self._grid_resolution
                    test_y = y1
                    while (forward and test_y <= y2) or (not forward and test_y >= y2):
                        if not self.field_polygon.contains_point(test_x, test_y) or \
                           self._is_point_in_obstacle(test_x, test_y):
                            clear = False
                            break
                        test_y += step
                    
                    if clear:
                        safe_x = test_x
                        break
                
                if safe_x is not None:
                    if self.field_polygon.contains_point(safe_x, y1):
                        path.append((safe_x, y1))
                    step = self._grid_resolution if forward else -self._grid_resolution
                    y = y1 + step
                    while (forward and y < y2) or (not forward and y > y2):
                        if self.field_polygon.contains_point(safe_x, y):
                            path.append((safe_x, y))
                        y += step
                    if self.field_polygon.contains_point(safe_x, y2):
                        path.append((safe_x, y2))
                    if self.field_polygon.contains_point(x, y2):
                        path.append((x, y2))
                    break
        
        return path
    
    def _connect_path_avoiding_obstacles(self, existing_path: List[Tuple[float, float]],
                                          new_path: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Ikki yo'lni to'siqlardan qochib ulash - FAQAT maydon ichida"""
        if not existing_path or not new_path:
            return new_path
        
        last_point = existing_path[-1]
        first_point = new_path[0]
        
        # To'g'ridan-to'g'ri ulanish mumkinmi?
        if not self._line_intersects_obstacle(last_point, first_point) and \
           self._line_inside_field(last_point, first_point):
            return new_path
        
        # Aylanib o'tish kerak - faqat maydon ichida
        connection = self._find_connection_path(last_point, first_point)
        return connection + new_path
    
    def _line_intersects_obstacle(self, p1: Tuple[float, float], 
                                   p2: Tuple[float, float]) -> bool:
        """Chiziq to'siq bilan kesishadimi?"""
        steps = int(np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) / self._grid_resolution) + 1
        
        for i in range(steps + 1):
            t = i / max(steps, 1)
            x = p1[0] + t * (p2[0] - p1[0])
            y = p1[1] + t * (p2[1] - p1[1])
            if self._is_point_in_obstacle(x, y):
                return True
        return False
    
    def _line_inside_field(self, p1: Tuple[float, float], 
                           p2: Tuple[float, float]) -> bool:
        """Chiziq butunlay maydon ichidami?"""
        steps = int(np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) / self._grid_resolution) + 1
        
        for i in range(steps + 1):
            t = i / max(steps, 1)
            x = p1[0] + t * (p2[0] - p1[0])
            y = p1[1] + t * (p2[1] - p1[1])
            if not self.field_polygon.contains_point(x, y):
                return False
        return True
    
    def _find_connection_path(self, start: Tuple[float, float], 
                               end: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Ikki nuqta orasida to'siqlardan qochib yo'l topish - FAQAT maydon ichida"""
        # Oddiy usul: yuqoriga yoki pastga siljish
        path = []
        
        for direction in [1, -1]:
            for i in range(1, 20):
                offset = direction * i * self.row_spacing
                mid_y = (start[1] + end[1]) / 2 + offset
                
                p1 = (start[0], mid_y)
                p2 = (end[0], mid_y)
                
                # Butun yo'l maydon ichida va to'siqsiz bo'lishi kerak
                if (self.field_polygon.contains_point(p1[0], p1[1]) and
                    self.field_polygon.contains_point(p2[0], p2[1]) and
                    self._line_inside_field(start, p1) and
                    self._line_inside_field(p1, p2) and
                    self._line_inside_field(p2, end) and
                    not self._line_intersects_obstacle(start, p1) and
                    not self._line_intersects_obstacle(p1, p2) and
                    not self._line_intersects_obstacle(p2, end)):
                    
                    path = [p1, p2]
                    return path
        
        # Agar to'g'ri yo'l topilmasa, maydon chegarasi bo'ylab yurish
        path = self._find_boundary_path(start, end)
        return path
    
    def _find_boundary_path(self, start: Tuple[float, float], 
                            end: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Maydon chegarasi bo'ylab yo'l topish"""
        path = []
        vertices = self.field_polygon.vertices
        n = len(vertices)
        
        # Eng yaqin chegara nuqtasini topish
        def find_nearest_boundary_point(point: Tuple[float, float]) -> Tuple[float, float]:
            best_point = point
            best_dist = float('inf')
            
            for i in range(n):
                v1 = vertices[i]
                v2 = vertices[(i + 1) % n]
                
                # Nuqtadan qirraga eng yaqin nuqta
                dx = v2[0] - v1[0]
                dy = v2[1] - v1[1]
                length_sq = dx * dx + dy * dy
                
                if length_sq > 0:
                    t = max(0, min(1, ((point[0] - v1[0]) * dx + (point[1] - v1[1]) * dy) / length_sq))
                    nearest = (v1[0] + t * dx, v1[1] + t * dy)
                else:
                    nearest = v1
                
                dist = np.sqrt((point[0] - nearest[0])**2 + (point[1] - nearest[1])**2)
                if dist < best_dist:
                    best_dist = dist
                    best_point = nearest
            
            return best_point
        
        # Chegaraga yaqin nuqtalarni topish
        start_boundary = find_nearest_boundary_point(start)
        end_boundary = find_nearest_boundary_point(end)
        
        # Start -> boundary -> end
        if self.field_polygon.contains_point(start_boundary[0], start_boundary[1]):
            path.append(start_boundary)
        if self.field_polygon.contains_point(end_boundary[0], end_boundary[1]):
            path.append(end_boundary)
        
        return path


# Test
if __name__ == "__main__":
    # Beshburchak maydon
    field = FieldPolygon(
        vertices=[
            (0, 0),
            (50, 0),
            (60, 30),
            (30, 50),
            (0, 40)
        ],
        name="Beshburchak dala"
    )
    
    print(f"Maydon: {field.name}")
    print(f"Yuza: {field.get_area():.2f} m²")
    print(f"Chegaralar: {field.get_bounds()}")
    
    # Planner
    planner = CoveragePathPlanner(field, working_width=3.0, overlap=0.1)
    
    # To'siq qo'shish
    planner.add_obstacle(Obstacle(
        obstacle_id=0,
        obstacle_type=ObstacleType.TREE,
        position=(25, 20),
        size=(5, 5)
    ))
    
    # Boustrophedon
    result = planner.plan_boustrophedon(start_corner="bottom_left")
    
    print(f"\nBoustrophedon natijasi:")
    print(f"  Yo'l nuqtalari: {len(result.path)}")
    print(f"  Umumiy masofa: {result.total_distance:.2f} m")
    print(f"  Qoplangan: {result.coverage_percentage:.1f}%")
    print(f"  Qatorlar: {result.num_rows}")
    print(f"  Vaqt: {result.computation_time*1000:.2f} ms")
