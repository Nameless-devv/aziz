"""
Environment Modeling Module
===========================

Dala muhitini raqamli xarita ko'rinishida modellashtiradi.
Grid-based map yoki occupancy grid model ishlatiladi.

Vazifalar:
- 2D/3D muhit xaritasini yaratish
- O'simlik qatorlari, sug'orish kanallari, toshlar va boshqa to'siqlarni belgilash
- Occupancy grid modelini boshqarish

Kirish:
- Xarita o'lchamlari (width, height)
- Cell o'lchami (resolution)
- To'siqlar ro'yxati

Chiqish:
- Grid-based occupancy map
- To'siqlar xaritasi
- Navigatsiya uchun tayyor muhit modeli
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any
import yaml


class ObstacleType(Enum):
    """To'siq turlari"""
    FREE = 0           # Bo'sh joy
    CROP_ROW = 1       # O'simlik qatori
    IRRIGATION = 2     # Sug'orish kanali
    ROCK = 3           # Tosh
    TREE = 4           # Daraxt
    BUILDING = 5       # Bino
    TEMPORARY = 6      # Vaqtinchalik to'siq
    UNKNOWN = 7        # Noma'lum


@dataclass
class GridCell:
    """
    Grid hujayra ma'lumotlari
    
    Attributes:
        x: Hujayra x koordinatasi (grid indeksi)
        y: Hujayra y koordinatasi (grid indeksi)
        obstacle_type: To'siq turi
        occupancy: Band qilinganlik darajasi (0.0 - 1.0)
        height: Balandlik (3D model uchun)
        cost: Harakat qiymati
        metadata: Qo'shimcha ma'lumotlar
    """
    x: int
    y: int
    obstacle_type: ObstacleType = ObstacleType.FREE
    occupancy: float = 0.0
    height: float = 0.0
    cost: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_passable(self) -> bool:
        """Hujayra o'tish mumkinligini tekshirish"""
        return self.occupancy < 0.5 and self.obstacle_type == ObstacleType.FREE
    
    def is_obstacle(self) -> bool:
        """Hujayra to'siq ekanligini tekshirish"""
        return self.occupancy >= 0.5 or self.obstacle_type != ObstacleType.FREE


@dataclass
class Obstacle:
    """
    To'siq ma'lumotlari
    
    Attributes:
        obstacle_id: Unikal identifikator
        obstacle_type: To'siq turi
        position: Markaz pozitsiyasi (x, y) metrda
        size: O'lcham (width, height) metrda
        shape: Shakl ('rectangle', 'circle', 'polygon')
        vertices: Polygon uchun nuqtalar
        is_dynamic: Dinamik to'siqmi
        radius: Doira to'siq radiusi
    """
    obstacle_id: int
    obstacle_type: ObstacleType
    position: Tuple[float, float]
    size: Tuple[float, float] = (1.0, 1.0)
    shape: str = 'rectangle'
    vertices: Optional[List[Tuple[float, float]]] = None
    is_dynamic: bool = False
    radius: float = 0.0  # Doira to'siq uchun radius
    
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """To'siqning chegaraviy qutisini qaytarish (x_min, y_min, x_max, y_max)"""
        if self.shape == 'circle':
            radius = max(self.size) / 2
            return (
                self.position[0] - radius,
                self.position[1] - radius,
                self.position[0] + radius,
                self.position[1] + radius
            )
        else:
            half_w = self.size[0] / 2
            half_h = self.size[1] / 2
            return (
                self.position[0] - half_w,
                self.position[1] - half_h,
                self.position[0] + half_w,
                self.position[1] + half_h
            )


class EnvironmentMap:
    """
    Muhit xaritasi klassi
    
    Dala muhitini 2D grid-based xarita sifatida modellashtiradi.
    Occupancy grid modeli ishlatiladi.
    
    Attributes:
        width: Xarita kengligi (metrda)
        height: Xarita balandligi (metrda)
        cell_size: Hujayra o'lchami (metrda)
        grid: Occupancy grid massivi
        obstacles: To'siqlar ro'yxati
    """
    
    def __init__(self, width: float = 100.0, height: float = 100.0, 
                 cell_size: float = 0.5, enable_3d: bool = False):
        """
        Muhit xaritasini yaratish
        
        Args:
            width: Xarita kengligi (metrda)
            height: Xarita balandligi (metrda)
            cell_size: Hujayra o'lchami (metrda)
            enable_3d: 3D modellashtirish
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.enable_3d = enable_3d
        
        # Grid o'lchamlarini hisoblash
        self.grid_width = int(np.ceil(width / cell_size))
        self.grid_height = int(np.ceil(height / cell_size))
        
        # Occupancy grid yaratish (0 = bo'sh, 1 = band)
        self.occupancy_grid = np.zeros((self.grid_height, self.grid_width), dtype=np.float32)
        
        # To'siq turlari gridi
        self.obstacle_type_grid = np.zeros((self.grid_height, self.grid_width), dtype=np.int8)
        
        # Cost grid (harakat qiymati)
        self.cost_grid = np.ones((self.grid_height, self.grid_width), dtype=np.float32)
        
        # 3D model uchun balandlik xaritasi
        if enable_3d:
            self.height_map = np.zeros((self.grid_height, self.grid_width), dtype=np.float32)
        else:
            self.height_map = None
        
        # To'siqlar ro'yxati
        self.obstacles: List[Obstacle] = []
        self._obstacle_id_counter = 0
        
        # Metadata
        self.metadata = {
            'created_at': None,
            'last_updated': None,
            'coordinate_system': 'local',
            'origin': (0.0, 0.0)
        }
    
    def world_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        """
        Dunyo koordinatalarini grid indekslariga aylantirish
        
        Args:
            x: X koordinatasi (metrda)
            y: Y koordinatasi (metrda)
            
        Returns:
            Grid indekslari (grid_x, grid_y)
        """
        grid_x = int(np.clip(x / self.cell_size, 0, self.grid_width - 1))
        grid_y = int(np.clip(y / self.cell_size, 0, self.grid_height - 1))
        return grid_x, grid_y
    
    def grid_to_world(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        """
        Grid indekslarini dunyo koordinatalariga aylantirish
        
        Args:
            grid_x: Grid X indeksi
            grid_y: Grid Y indeksi
            
        Returns:
            Dunyo koordinatalari (x, y) metrda
        """
        x = (grid_x + 0.5) * self.cell_size
        y = (grid_y + 0.5) * self.cell_size
        return x, y
    
    def is_valid_grid_position(self, grid_x: int, grid_y: int) -> bool:
        """Grid pozitsiyasi to'g'ri ekanligini tekshirish"""
        return 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height
    
    def is_valid_world_position(self, x: float, y: float) -> bool:
        """Dunyo pozitsiyasi xarita ichida ekanligini tekshirish"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def add_obstacle(self, obstacle: Obstacle) -> int:
        """
        To'siq qo'shish
        
        Args:
            obstacle: To'siq obyekti
            
        Returns:
            To'siq ID raqami
        """
        obstacle.obstacle_id = self._obstacle_id_counter
        self._obstacle_id_counter += 1
        self.obstacles.append(obstacle)
        
        # Occupancy gridni yangilash
        self._update_grid_with_obstacle(obstacle)
        
        return obstacle.obstacle_id
    
    def remove_obstacle(self, obstacle_id: int) -> bool:
        """
        To'siqni o'chirish
        
        Args:
            obstacle_id: To'siq ID raqami
            
        Returns:
            Muvaffaqiyatli o'chirilganligini bildiradi
        """
        for i, obs in enumerate(self.obstacles):
            if obs.obstacle_id == obstacle_id:
                self._clear_grid_obstacle(obs)
                self.obstacles.pop(i)
                return True
        return False
    
    def _update_grid_with_obstacle(self, obstacle: Obstacle):
        """To'siqni gridga qo'shish"""
        bbox = obstacle.get_bounding_box()
        
        # Grid indekslarini hisoblash
        min_gx, min_gy = self.world_to_grid(bbox[0], bbox[1])
        max_gx, max_gy = self.world_to_grid(bbox[2], bbox[3])
        
        # Grid hujayralarini belgilash
        for gy in range(min_gy, max_gy + 1):
            for gx in range(min_gx, max_gx + 1):
                if self.is_valid_grid_position(gx, gy):
                    # Hujayra markazi to'siq ichida ekanligini tekshirish
                    cell_x, cell_y = self.grid_to_world(gx, gy)
                    
                    if self._point_in_obstacle(cell_x, cell_y, obstacle):
                        self.occupancy_grid[gy, gx] = 1.0
                        self.obstacle_type_grid[gy, gx] = obstacle.obstacle_type.value
                        self.cost_grid[gy, gx] = float('inf')
    
    def _clear_grid_obstacle(self, obstacle: Obstacle):
        """To'siqni griddan o'chirish"""
        bbox = obstacle.get_bounding_box()
        
        min_gx, min_gy = self.world_to_grid(bbox[0], bbox[1])
        max_gx, max_gy = self.world_to_grid(bbox[2], bbox[3])
        
        for gy in range(min_gy, max_gy + 1):
            for gx in range(min_gx, max_gx + 1):
                if self.is_valid_grid_position(gx, gy):
                    self.occupancy_grid[gy, gx] = 0.0
                    self.obstacle_type_grid[gy, gx] = ObstacleType.FREE.value
                    self.cost_grid[gy, gx] = 1.0
    
    def _point_in_obstacle(self, x: float, y: float, obstacle: Obstacle) -> bool:
        """Nuqta to'siq ichida ekanligini tekshirish"""
        if obstacle.shape == 'circle':
            radius = max(obstacle.size) / 2
            dist = np.sqrt((x - obstacle.position[0])**2 + (y - obstacle.position[1])**2)
            return dist <= radius
        else:  # rectangle
            half_w = obstacle.size[0] / 2
            half_h = obstacle.size[1] / 2
            return (abs(x - obstacle.position[0]) <= half_w and 
                    abs(y - obstacle.position[1]) <= half_h)
    
    def is_cell_free(self, grid_x: int, grid_y: int) -> bool:
        """Hujayra bo'sh ekanligini tekshirish"""
        if not self.is_valid_grid_position(grid_x, grid_y):
            return False
        return self.occupancy_grid[grid_y, grid_x] < 0.5
    
    def is_position_free(self, x: float, y: float) -> bool:
        """Dunyo pozitsiyasi bo'sh ekanligini tekshirish"""
        grid_x, grid_y = self.world_to_grid(x, y)
        return self.is_cell_free(grid_x, grid_y)
    
    def get_cell(self, grid_x: int, grid_y: int) -> Optional[GridCell]:
        """Grid hujayrasini olish"""
        if not self.is_valid_grid_position(grid_x, grid_y):
            return None
        
        return GridCell(
            x=grid_x,
            y=grid_y,
            obstacle_type=ObstacleType(self.obstacle_type_grid[grid_y, grid_x]),
            occupancy=self.occupancy_grid[grid_y, grid_x],
            height=self.height_map[grid_y, grid_x] if self.height_map is not None else 0.0,
            cost=self.cost_grid[grid_y, grid_x]
        )
    
    def inflate_obstacles(self, inflation_radius: float):
        """
        To'siqlarni kengaytirish (robot o'lchami uchun)
        
        Args:
            inflation_radius: Kengaytirish radiusi (metrda)
        """
        inflation_cells = int(np.ceil(inflation_radius / self.cell_size))
        
        # Yangi inflated grid yaratish
        inflated_grid = self.occupancy_grid.copy()
        inflated_cost = self.cost_grid.copy()
        
        # Har bir to'siq hujayrasi uchun
        obstacle_positions = np.where(self.occupancy_grid >= 0.5)
        
        for gy, gx in zip(obstacle_positions[0], obstacle_positions[1]):
            # Atrofdagi hujayralarni belgilash
            for dy in range(-inflation_cells, inflation_cells + 1):
                for dx in range(-inflation_cells, inflation_cells + 1):
                    new_gx = gx + dx
                    new_gy = gy + dy
                    
                    if self.is_valid_grid_position(new_gx, new_gy):
                        # Masofani hisoblash
                        dist = np.sqrt(dx**2 + dy**2) * self.cell_size
                        
                        if dist <= inflation_radius:
                            inflated_grid[new_gy, new_gx] = max(
                                inflated_grid[new_gy, new_gx],
                                1.0 - dist / inflation_radius
                            )
                            # Cost gradiyenti
                            if dist > 0:
                                inflated_cost[new_gy, new_gx] = max(
                                    inflated_cost[new_gy, new_gx],
                                    1.0 + (inflation_radius - dist) / inflation_radius * 10
                                )
        
        self.occupancy_grid = inflated_grid
        self.cost_grid = inflated_cost
    
    def add_crop_rows(self, start_x: float, start_y: float, 
                      row_count: int, row_length: float,
                      row_spacing: float, row_width: float = 0.3):
        """
        O'simlik qatorlarini qo'shish
        
        Args:
            start_x: Boshlang'ich X koordinatasi
            start_y: Boshlang'ich Y koordinatasi
            row_count: Qatorlar soni
            row_length: Qator uzunligi
            row_spacing: Qatorlar orasidagi masofa
            row_width: Qator kengligi
        """
        for i in range(row_count):
            y = start_y + i * row_spacing
            obstacle = Obstacle(
                obstacle_id=0,
                obstacle_type=ObstacleType.CROP_ROW,
                position=(start_x + row_length / 2, y),
                size=(row_length, row_width),
                shape='rectangle'
            )
            self.add_obstacle(obstacle)
    
    def add_irrigation_channel(self, start: Tuple[float, float], 
                               end: Tuple[float, float], width: float = 0.5):
        """
        Sug'orish kanalini qo'shish
        
        Args:
            start: Boshlang'ich nuqta (x, y)
            end: Oxirgi nuqta (x, y)
            width: Kanal kengligi
        """
        # Kanal uzunligi va yo'nalishi
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = np.sqrt(dx**2 + dy**2)
        
        center_x = (start[0] + end[0]) / 2
        center_y = (start[1] + end[1]) / 2
        
        obstacle = Obstacle(
            obstacle_id=0,
            obstacle_type=ObstacleType.IRRIGATION,
            position=(center_x, center_y),
            size=(length, width),
            shape='rectangle'
        )
        self.add_obstacle(obstacle)
    
    def add_random_rocks(self, count: int, min_size: float = 0.2, 
                         max_size: float = 1.0, margin: float = 5.0):
        """
        Tasodifiy toshlar qo'shish
        
        Args:
            count: Toshlar soni
            min_size: Minimal o'lcham
            max_size: Maksimal o'lcham
            margin: Chegaradan masofa
        """
        for _ in range(count):
            size = np.random.uniform(min_size, max_size)
            x = np.random.uniform(margin, self.width - margin)
            y = np.random.uniform(margin, self.height - margin)
            
            obstacle = Obstacle(
                obstacle_id=0,
                obstacle_type=ObstacleType.ROCK,
                position=(x, y),
                size=(size, size),
                shape='circle'
            )
            self.add_obstacle(obstacle)
    
    def get_neighbors(self, grid_x: int, grid_y: int, 
                      allow_diagonal: bool = True) -> List[Tuple[int, int, float]]:
        """
        Qo'shni hujayralarni olish
        
        Args:
            grid_x: Hujayra X indeksi
            grid_y: Hujayra Y indeksi
            allow_diagonal: Diagonal harakatga ruxsat
            
        Returns:
            Qo'shnilar ro'yxati (x, y, cost)
        """
        neighbors = []
        
        # 4 asosiy yo'nalish
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # 8 yo'nalish (diagonal qo'shiladi)
        if allow_diagonal:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            new_x = grid_x + dx
            new_y = grid_y + dy
            
            if self.is_valid_grid_position(new_x, new_y):
                if self.is_cell_free(new_x, new_y):
                    # Diagonal harakat qiymati
                    if dx != 0 and dy != 0:
                        move_cost = 1.414 * self.cost_grid[new_y, new_x]
                    else:
                        move_cost = self.cost_grid[new_y, new_x]
                    
                    neighbors.append((new_x, new_y, move_cost))
        
        return neighbors
    
    def save_to_file(self, filename: str):
        """Xaritani faylga saqlash"""
        data = {
            'width': self.width,
            'height': self.height,
            'cell_size': self.cell_size,
            'occupancy_grid': self.occupancy_grid.tolist(),
            'obstacle_type_grid': self.obstacle_type_grid.tolist(),
            'obstacles': [
                {
                    'id': obs.obstacle_id,
                    'type': obs.obstacle_type.value,
                    'position': obs.position,
                    'size': obs.size,
                    'shape': obs.shape
                }
                for obs in self.obstacles
            ]
        }
        
        with open(filename, 'w') as f:
            yaml.dump(data, f)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'EnvironmentMap':
        """Xaritani fayldan yuklash"""
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        
        env_map = cls(
            width=data['width'],
            height=data['height'],
            cell_size=data['cell_size']
        )
        
        env_map.occupancy_grid = np.array(data['occupancy_grid'], dtype=np.float32)
        env_map.obstacle_type_grid = np.array(data['obstacle_type_grid'], dtype=np.int8)
        
        for obs_data in data.get('obstacles', []):
            obstacle = Obstacle(
                obstacle_id=obs_data['id'],
                obstacle_type=ObstacleType(obs_data['type']),
                position=tuple(obs_data['position']),
                size=tuple(obs_data['size']),
                shape=obs_data['shape']
            )
            env_map.obstacles.append(obstacle)
        
        return env_map
    
    def create_agricultural_field(self, field_type: str = 'standard'):
        """
        Standart qishloq xo'jaligi dalasini yaratish
        
        Args:
            field_type: Dala turi ('standard', 'vineyard', 'orchard')
        """
        if field_type == 'standard':
            # O'simlik qatorlari
            self.add_crop_rows(
                start_x=10, start_y=10,
                row_count=15, row_length=80,
                row_spacing=4, row_width=0.5
            )
            
            # Sug'orish kanallari
            self.add_irrigation_channel((5, 5), (5, 95), width=1.0)
            self.add_irrigation_channel((95, 5), (95, 95), width=1.0)
            
            # Tasodifiy toshlar
            self.add_random_rocks(count=10, min_size=0.3, max_size=0.8)
            
        elif field_type == 'vineyard':
            # Uzum qatorlari (yanada zich)
            self.add_crop_rows(
                start_x=5, start_y=5,
                row_count=30, row_length=90,
                row_spacing=2.5, row_width=0.4
            )
            
        elif field_type == 'orchard':
            # Bog' (daraxtlar)
            spacing = 8
            for x in range(10, int(self.width) - 10, spacing):
                for y in range(10, int(self.height) - 10, spacing):
                    obstacle = Obstacle(
                        obstacle_id=0,
                        obstacle_type=ObstacleType.TREE,
                        position=(x, y),
                        size=(2.0, 2.0),
                        shape='circle'
                    )
                    self.add_obstacle(obstacle)
    
    def __repr__(self) -> str:
        return (f"EnvironmentMap(width={self.width}m, height={self.height}m, "
                f"cell_size={self.cell_size}m, grid={self.grid_width}x{self.grid_height}, "
                f"obstacles={len(self.obstacles)})")


# Test uchun
if __name__ == "__main__":
    # Muhit xaritasini yaratish
    env_map = EnvironmentMap(width=50, height=50, cell_size=0.5)
    
    # Qishloq xo'jaligi dalasini yaratish
    env_map.create_agricultural_field('standard')
    
    # Robot o'lchami uchun to'siqlarni kengaytirish
    env_map.inflate_obstacles(inflation_radius=0.5)
    
    print(env_map)
    print(f"Bo'sh hujayralar soni: {np.sum(env_map.occupancy_grid < 0.5)}")
    print(f"To'siq hujayralar soni: {np.sum(env_map.occupancy_grid >= 0.5)}")
