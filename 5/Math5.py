import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

matplotlib.use('TkAgg')


# Задание 1: Построение тепловой карты
def plot_heatmap():
    # Создаем сетку 20x20 с температурными значениями в диапазоне [-20, 30]
    data = np.random.uniform(-20, 30, (20, 20))

    fig = Figure(figsize=(8, 6))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    cax = ax.imshow(data, cmap='hot', interpolation='nearest')
    fig.colorbar(cax, ax=ax, label='Temperature')
    ax.set_title('Heatmap of Temperature Distribution')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    canvas.print_figure('heatmap.png')


# Задание 2: Визуализация волнового фронта
def animate_wave():
    # Параметры волны
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x)

    fig = Figure(figsize=(8, 6))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    line, = ax.plot(x, y)

    def update(frame):
        line.set_ydata(np.sin(x + frame / 10.0))
        return line,

    ani = FuncAnimation(fig, update, frames=range(100), blit=True)
    ax.set_title('1D Wave Propagation')
    ax.set_xlabel('X')
    ax.set_ylabel('Amplitude')
    canvas.print_figure('wave_animation.png')


# Выполнение заданий
plot_heatmap()
animate_wave()
