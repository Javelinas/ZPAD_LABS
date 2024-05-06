import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import iirfilter, lfilter

# Початкові параметри гармоніки та шуму
default_amplitude = 1
default_frequency = 1
default_phase = 0
default_noise_mean = 0
default_noise_covariance = 0.1

# Початкові параметри фільтра
default_cutoff_frequency = 10.0
default_filter_order = 4

# Згенерувати часову ось
t = np.linspace(0, 1, 1000)

# Глобальна змінна для зберігання шуму
current_noise = None

# Функція для генерації шуму
def generate_noise():
    global current_noise
    noise_mean = s_noise_mean.val
    noise_covariance = s_noise_covariance.val
    current_noise = noise_mean * np.random.normal(0, np.sqrt(noise_covariance), t.shape)

# Функція, яка оновлює графік та інші елементи інтерфейсу
def update_plot(val=None):
    amplitude = s_amplitude.val
    frequency = s_frequency.val
    phase = s_phase.val
    show_noise = check_show_noise.get_status()[0]

    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        if current_noise is None:
            generate_noise()
        signal = harmonic + current_noise
    else:
        signal = harmonic

    ax.clear()
    ax.plot(t, signal, label='Гармоніка з шумом' if show_noise else 'Чиста гармоніка')
    ax.set_xlabel('Час')
    ax.set_ylabel('Сигнал')
    ax.legend()
    ax.grid(True)
    
    # Оновлення сигналу після фільтрації
    filtered_signal = filter_signal(signal)
    ax.plot(t, filtered_signal, label='Відфільтрований сигнал', color='red')
    ax.legend()
    
    plt.draw()

# Функція для фільтрації сигналу
def filter_signal(signal):
    fs = 1.0 / (t[1] - t[0])
    cutoff_frequency = s_cutoff_frequency.val
    filter_order = int(s_filter_order.val)
    b, a = iirfilter(filter_order, 2 * cutoff_frequency / fs, btype='lowpass')
    return lfilter(b, a, signal)

# Загальні вікно та елементи інтерфейсу
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.6)

# Створення слайдерів
axcolor = 'lightgoldenrodyellow'
ax_amplitude = plt.axes([0.1, 0.5, 0.65, 0.03], facecolor=axcolor)
ax_frequency = plt.axes([0.1, 0.45, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.4, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.1, 0.35, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.1, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_cutoff_frequency = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_filter_order = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)

s_amplitude = Slider(ax_amplitude, 'Амплітуда', 0.1, 10.0, valinit=default_amplitude)
s_frequency = Slider(ax_frequency, 'Частота', 0.1, 10.0, valinit=default_frequency)
s_phase = Slider(ax_phase, 'Фаза', 0, 2*np.pi, valinit=default_phase)
s_noise_mean = Slider(ax_noise_mean, 'Амплітуда шуму', -1.0, 1.0, valinit=default_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Дисперсія шуму', 0.0, 1.0, valinit=default_noise_covariance)
s_cutoff_frequency = Slider(ax_cutoff_frequency, 'Частота зрізу', 0.1, 20.0, valinit=default_cutoff_frequency)
s_filter_order = Slider(ax_filter_order, 'Порядок фільтру', 1, 10, valinit=default_filter_order, valstep=1)

# Функція для оновлення графіку при русі слайдерів амплітуди, частоти та фази
def update_signal(val):
    update_plot()
s_amplitude.on_changed(update_signal)
s_frequency.on_changed(update_signal)
s_phase.on_changed(update_signal)

# Функція для оновлення шуму при русі слайдерів амплітуди та дисперсії шуму
def update_noise(val):
    generate_noise()
    update_plot()
s_noise_mean.on_changed(update_noise)
s_noise_covariance.on_changed(update_noise)

# Функція для оновлення фільтра після зміни значень слайдерів
def update_filter(val):
    update_plot()
s_cutoff_frequency.on_changed(update_filter)
s_filter_order.on_changed(update_filter)

# Кнопка для показу/приховування шуму
ax_show_noise = plt.axes([0.8, 0.15, 0.1, 0.04])
check_show_noise = CheckButtons(ax_show_noise, ['Показати шум'], [True])
def show_noise(label):
    update_plot()
check_show_noise.on_clicked(show_noise)

# Кнопка Reset
ax_reset = plt.axes([0.8, 0.1, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    s_amplitude.reset()
    s_frequency.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_frequency.reset()
    s_filter_order.reset()

button_reset.on_clicked(reset)

update_plot()  # Викликаємо один раз, щоб відобразити початковий графік
plt.show()
