# Qishloq Xo'jaligi Roboti Path Planning Tizimi
## Arxitektura Hujjati

### 1. Umumiy Ko'rinish

Bu hujjat qishloq xo'jaligi robotlari uchun Path Planning tizimining arxitekturasini tavsiflaydi. Tizim modul asosida ishlab chiqilgan bo'lib, har bir modul mustaqil vazifalarni bajaradi.

### 2. Tizim Arxitekturasi

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AGRICULTURAL ROBOT PATH PLANNING SYSTEM                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────────┐                                                        │
│   │    Config      │ ◄── settings.yaml                                      │
│   │    Manager     │                                                         │
│   └───────┬────────┘                                                        │
│           │                                                                  │
│   ┌───────▼────────┐    ┌──────────────────┐    ┌──────────────────┐       │
│   │  Environment   │    │   Sensor Data    │    │    Obstacle      │       │
│   │  Modeling      │◄───│   Integration    │───►│   Detection &    │       │
│   │  Module        │    │   Module         │    │   Mapping        │       │
│   │                │    │                  │    │                  │       │
│   │ • Grid Map     │    │ • LiDAR          │    │ • Clustering     │       │
│   │ • Obstacles    │    │ • GPS            │    │ • Classification │       │
│   │ • Inflation    │    │ • Ultrasonic     │    │ • Tracking       │       │
│   └───────┬────────┘    └──────────────────┘    └────────┬─────────┘       │
│           │                                               │                  │
│           │              ┌──────────────────┐             │                  │
│           └─────────────►│   Path Planning  │◄────────────┘                  │
│                          │   Module         │                                │
│                          │                  │                                │
│                          │ • A* Algorithm   │                                │
│                          │ • Dijkstra       │                                │
│                          │ • RRT / RRT*     │                                │
│                          │ • Path Smoothing │                                │
│                          └────────┬─────────┘                                │
│                                   │                                          │
│           ┌───────────────────────┼───────────────────────┐                  │
│           ▼                       ▼                       ▼                  │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│   │  Motion Control  │    │   Simulation &   │    │   Evaluation &   │      │
│   │  Module          │    │   Visualization  │    │   Optimization   │      │
│   │                  │    │                  │    │                  │      │
│   │ • PID Controller │    │ • Matplotlib     │    │ • Path Length    │      │
│   │ • Pure Pursuit   │    │ • Animation      │    │ • Time Analysis  │      │
│   │ • Diff. Drive    │    │ • Real-time      │    │ • Energy Est.    │      │
│   └──────────────────┘    └──────────────────┘    └──────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3. Modullar Tavsifi

#### 3.1 Environment Modeling Module
**Fayl:** `src/environment_modeling.py`

**Vazifa:** Dala muhitini raqamli xarita ko'rinishida modellashtiradi.

**Asosiy Klasslar:**
- `EnvironmentMap` - Asosiy xarita klassi
- `GridCell` - Grid hujayra ma'lumotlari
- `Obstacle` - To'siq ma'lumotlari
- `ObstacleType` - To'siq turlari (Enum)

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| width | float | Xarita kengligi (metr) |
| height | float | Xarita balandligi (metr) |
| cell_size | float | Grid hujayra o'lchami (metr) |
| enable_3d | bool | 3D modellashtirish |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| occupancy_grid | np.ndarray | Band qilinganlik xaritasi |
| obstacle_type_grid | np.ndarray | To'siq turlari xaritasi |
| cost_grid | np.ndarray | Harakat qiymati xaritasi |
| obstacles | List[Obstacle] | To'siqlar ro'yxati |

**Asosiy Metodlar:**
```python
world_to_grid(x, y) -> Tuple[int, int]
grid_to_world(grid_x, grid_y) -> Tuple[float, float]
add_obstacle(obstacle) -> int
remove_obstacle(obstacle_id) -> bool
inflate_obstacles(radius)
get_neighbors(grid_x, grid_y) -> List[Tuple[int, int, float]]
```

---

#### 3.2 Sensor Data Integration Module
**Fayl:** `src/sensor_integration.py`

**Vazifa:** Robot sensorlaridan ma'lumotlarni qabul qiladi va integratsiya qiladi.

**Asosiy Klasslar:**
- `SensorManager` - Sensorlarni boshqarish
- `LidarSensor` - LiDAR sensori
- `GPSSensor` - GPS sensori
- `UltrasonicSensor` - Ultratovush sensori
- `CameraSensor` - Kamera sensori
- `IMUSensor` - IMU sensori

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| sensor_config | Dict | Sensor konfiguratsiyasi |
| robot_position | Tuple | Robot pozitsiyasi |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| point_cloud | PointCloud | LiDAR nuqtalar buluti |
| gps_data | GPSData | GPS ma'lumotlari |
| sensor_readings | Dict | Barcha sensor o'qishlari |

**LiDAR Parametrlari:**
- `range_max`: 30 metr
- `angle_range`: 360°
- `resolution`: 0.5°
- `noise_std`: 0.02 metr

---

#### 3.3 Obstacle Detection and Mapping Module
**Fayl:** `src/obstacle_detection.py`

**Vazifa:** Sensor ma'lumotlarini qayta ishlab to'siqlarni aniqlaydi.

**Asosiy Klasslar:**
- `ObstacleDetector` - To'siq aniqlash
- `DetectedObstacle` - Aniqlangan to'siq
- `ObstacleClassification` - To'siq klassifikatsiyasi

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| point_cloud | PointCloud | LiDAR nuqtalar |
| robot_position | Tuple | Robot pozitsiyasi |
| env_map | EnvironmentMap | Muhit xaritasi |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| detected_obstacles | List[DetectedObstacle] | Aniqlangan to'siqlar |
| updated_map | EnvironmentMap | Yangilangan xarita |

**Algoritm:** DBSCAN klasterlash
- `eps`: 0.3 metr
- `min_points`: 3

---

#### 3.4 Path Planning Module
**Fayl:** `src/path_planning.py`

**Vazifa:** Robot uchun optimal yo'lni hisoblaydi.

**Asosiy Klasslar:**
- `PathPlanner` - Yuqori darajali planner
- `AStarPlanner` - A* algoritmi
- `DijkstraPlanner` - Dijkstra algoritmi
- `RRTPlanner` - RRT algoritmi
- `RRTStarPlanner` - RRT* algoritmi

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| env_map | EnvironmentMap | Muhit xaritasi |
| start | Tuple[float, float] | Boshlang'ich nuqta |
| goal | Tuple[float, float] | Maqsad nuqta |
| algorithm | PlanningAlgorithm | Algoritm turi |
| heuristic | HeuristicType | Heuristic funksiya |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| path | List[Tuple[int, int]] | Grid yo'li |
| path_world | List[Tuple[float, float]] | Dunyo yo'li |
| path_length | float | Yo'l uzunligi (metr) |
| computation_time | float | Hisoblash vaqti (s) |
| nodes_explored | int | Tekshirilgan tugunlar |
| success | bool | Muvaffaqiyat |

**Algoritmlar:**

**A* Algorithm:**
```
f(n) = g(n) + h(n)
g(n) - startdan n ga real masofa
h(n) - n dan goalga taxminiy masofa (heuristic)
```

**Heuristic Funksiyalar:**
- Euclidean: `√((x2-x1)² + (y2-y1)²)`
- Manhattan: `|x2-x1| + |y2-y1|`
- Diagonal: `max(dx, dy) + (√2-1) * min(dx, dy)`

---

#### 3.5 Motion Control Module
**Fayl:** `src/motion_control.py`

**Vazifa:** Topilgan yo'l bo'yicha robot harakatini boshqaradi.

**Asosiy Klasslar:**
- `MotionController` - Harakat boshqaruvi
- `DifferentialDriveRobot` - Differential drive model
- `PIDController` - PID controller
- `RobotState` - Robot holati

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| path | List[Tuple] | Yo'l nuqtalari |
| robot_state | RobotState | Joriy holat |
| dt | float | Vaqt oralig'i |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| velocity_cmd | VelocityCommand | Tezlik buyrug'i |
| wheel_velocities | WheelVelocities | G'ildirak tezliklari |
| updated_state | RobotState | Yangi holat |

**Robot Parametrlari:**
- `wheel_base`: 0.5 metr
- `max_linear_velocity`: 2.0 m/s
- `max_angular_velocity`: 1.5 rad/s

**PID Parametrlari:**
| Controller | Kp | Ki | Kd |
|------------|----|----|-----|
| Linear | 1.0 | 0.1 | 0.05 |
| Angular | 2.0 | 0.2 | 0.1 |

---

#### 3.6 Simulation and Visualization Module
**Fayl:** `src/simulation.py`

**Vazifa:** Robot harakatini simulyatsiya qilish va vizualizatsiya.

**Asosiy Klasslar:**
- `Simulator` - Simulyator
- `Visualizer` - Vizualizator
- `SimulationScenario` - Test stsenariylari

**Kirish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| env_map | EnvironmentMap | Muhit xaritasi |
| controller | MotionController | Harakat controller |
| path | List[Tuple] | Yo'l |

**Chiqish Ma'lumotlari:**
| Parametr | Tur | Tavsif |
|----------|-----|--------|
| visualization | Figure | Matplotlib rasm |
| animation | Animation | Animatsiya |
| trajectory | List[Tuple] | Robot traektoriyasi |

**Stsenariylar:**
- `simple` - Oddiy dala (50x50m)
- `agricultural` - Qishloq xo'jaligi (100x100m)
- `vineyard` - Uzumzor (80x80m)
- `orchard` - Bog' (100x100m)

---

#### 3.7 Evaluation and Optimization Module
**Fayl:** `src/evaluation.py`

**Vazifa:** Algoritm samaradorligini baholash.

**Asosiy Klasslar:**
- `Evaluator` - Baholovchi
- `PathMetrics` - Yo'l metrikalari
- `TrajectoryMetrics` - Traektoriya metrikalari
- `OptimizationAdvisor` - Tavsiyalar

**Baholash Metrikalari:**
| Metrika | Tavsif | Birlik |
|---------|--------|--------|
| path_length | Yo'l uzunligi | metr |
| computation_time | Hisoblash vaqti | sekund |
| nodes_explored | Tekshirilgan tugunlar | son |
| path_smoothness | Silliqlik | 0-1 |
| min_obstacle_distance | Min to'siq masofasi | metr |
| energy_estimate | Energiya sarfi | Joule |

---

### 4. Ma'lumotlar Oqimi

```
┌──────────┐     ┌───────────┐     ┌───────────┐
│  Sensor  │────►│  Obstacle │────►│ Environment│
│  Data    │     │  Detection│     │    Map     │
└──────────┘     └───────────┘     └─────┬─────┘
                                         │
                                         ▼
┌──────────┐     ┌───────────┐     ┌───────────┐
│  Motion  │◄────│   Path    │◄────│   Path    │
│ Commands │     │  Planning │     │  Request  │
└────┬─────┘     └───────────┘     └───────────┘
     │
     ▼
┌──────────┐     ┌───────────┐
│  Robot   │────►│Evaluation │
│  State   │     │  Metrics  │
└──────────┘     └───────────┘
```

---

### 5. API Interfeysi

#### Path Planning
```python
from src.path_planning import PathPlanner, PlanningAlgorithm

# Planner yaratish
planner = PathPlanner(env_map, PlanningAlgorithm.A_STAR)

# Yo'l rejalashtirish
result = planner.plan(start=(5, 5), goal=(45, 45))

# Natija
if result.success:
    path = result.path_world
    length = result.path_length
```

#### Simulyatsiya
```python
from src.simulation import Simulator

# Simulator yaratish
simulator = Simulator(env_map, controller)
simulator.set_path(path)

# Ishga tushirish
simulator.run(animate=True)
```

#### Baholash
```python
from src.evaluation import Evaluator

# Baholash
evaluator = Evaluator(env_map)
metrics = evaluator.evaluate_path(result)

# Taqqoslash
comparison = evaluator.compare_algorithms(start, goal)
```

---

### 6. Kengaytirish Imkoniyatlari

#### 6.1 Yangi Algoritm Qo'shish
```python
from src.path_planning import BasePathPlanner

class CustomPlanner(BasePathPlanner):
    def plan(self, start, goal) -> PlanningResult:
        # Custom algoritm
        pass
```

#### 6.2 Yangi Sensor Qo'shish
```python
from src.sensor_integration import BaseSensor

class CustomSensor(BaseSensor):
    def read(self) -> SensorReading:
        # Sensor o'qish
        pass
    
    def configure(self, config):
        # Konfiguratsiya
        pass
```

---

### 7. Real Robot Integratsiyasi

Tizim ROS (Robot Operating System) bilan integratsiya qilish uchun tayyor:

```python
# ROS integratsiya misoli
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class ROSInterface:
    def __init__(self):
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
    
    def publish_velocity(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.cmd_pub.publish(twist)
```

---

### 8. Litsenziya

MIT License

Copyright (c) 2024 Agricultural Robotics Team
