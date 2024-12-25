import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Константы
num_particles = 100  # Количество частиц
speed_range = (1, 5)  # Диапазон скоростей
region_size = (20, 20)  # Размер региона для тепловой карты

# Генерация случайных данных о температуре
np.random.seed(0)  # Для воспроизводимости
temperature_data = np.random.uniform(-20, 30, region_size)  # Данные температуры в диапазоне [-20, 30]

# Инициализация частиц
angles = np.random.uniform(0, 2 * np.pi, num_particles)  # Случайные углы
speeds = np.random.uniform(speed_range[0], speed_range[1], num_particles)  # Случайные скорости
positions = np.zeros((num_particles, 2))  # Начальные позиции (все в центре)

# Создание фигуры и осей
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Настройка тепловой карты
heatmap = ax1.imshow(temperature_data, cmap='hot', interpolation='nearest', vmin=-20, vmax=30)
ax1.set_title('Тепловая карта температуры')
ax1.set_xlabel('X координата')
ax1.set_ylabel('Y координата')
plt.colorbar(heatmap, ax=ax1, label='Температура (°C)')

# Настройка графика для частиц
ax2.set_xlim(-10, 10)
ax2.set_ylim(-10, 10)
scatter = ax2.scatter(positions[:, 0], positions[:, 1])
ax2.set_title('Расхождение частиц от центра')
ax2.set_xlabel('X координата')
ax2.set_ylabel('Y координата')


# Функция обновления для анимации
def update(frame):
    global positions
    for i in range(num_particles):
        positions[i][0] += speeds[i] * np.cos(angles[i])  # Обновление x-координаты
        positions[i][1] += speeds[i] * np.sin(angles[i])  # Обновление y-координаты

    scatter.set_offsets(positions)  # Обновление позиций частиц

    return scatter,


# Анимация
ani = animation.FuncAnimation(fig, update, frames=100, interval=50)

plt.tight_layout()
plt.show()
