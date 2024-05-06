import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Slider, Toggle, Button
from bokeh.plotting import figure
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

# Set up plot
plot = figure(
    height=800, width=800, title="Графіки",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[0, 1],
    y_range=[-1, 1]
)

harmonic_source = ColumnDataSource(data=dict(x=t, y=t))
filtered_source = ColumnDataSource(data=dict(x=t, y=t))

plot.line('x', 'y', name="Гармоніка з шумом", source=harmonic_source, line_width=3, line_alpha=0.6)
plot.line('x', 'y', name="Відфільтрований сигнал", source=filtered_source, line_width=3, line_alpha=0.6, line_color="red")


# Функція для генерації шуму
def generate_noise():
    global current_noise
    noise_mean = s_noise_mean.value
    noise_covariance = s_noise_covariance.value
    current_noise = noise_mean * np.random.normal(0, np.sqrt(noise_covariance), t.shape)


# Функція, яка оновлює графік та інші елементи інтерфейсу
def update_plot(attr, old, new):
    amplitude = s_amplitude.value
    frequency = s_frequency.value
    phase = s_phase.value

    # Генеруємо гармоніку
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    
    # Додаємо шум, якщо відображення шуму активоване
    if check_show_noise.active:
        if current_noise is None:
            generate_noise()
        signal = harmonic + current_noise
    else:
        signal = harmonic

    # Оновлюємо межі по вертикалі відповідно до амплітуди сигналу
    plot.y_range.start = -amplitude
    plot.y_range.end = amplitude

    # Оновлюємо дані гармоніки та відфільтрованого сигналу
    harmonic_source.data = {
        "x": t,
        "y": signal
    }

    filtered_source.data = {
        "x": t,
        "y": filter_signal(signal)
    }


# Функція для фільтрації сигналу
def filter_signal(signal):
    fs = 1.0 / (t[1] - t[0])
    cutoff_frequency = s_cutoff_frequency.value
    filter_order = int(s_filter_order.value)
    b, a = iirfilter(filter_order, 2 * cutoff_frequency / fs, btype='lowpass')
    return lfilter(b, a, signal)


def update_noise(attr, old, new):
    generate_noise()
    update_plot(None, None, None)


def reset_values():
    # Скидуємо всі значення до початкових
    s_amplitude.value = default_amplitude
    s_frequency.value = default_frequency
    s_phase.value = default_phase
    s_noise_mean.value = default_noise_mean
    s_noise_covariance.value = default_noise_covariance
    s_cutoff_frequency.value = default_cutoff_frequency
    s_filter_order.value = default_filter_order
    check_show_noise.active = False


# Створюємо візуальні елементи інтерфейсу
s_amplitude = Slider(title='Амплітуда', start=0.1, end=10.0, value=default_amplitude, step=0.05)
s_frequency = Slider(title='Частота', start=0.1, end=10.0, value=default_frequency, step=0.05)
s_phase = Slider(title='Фаза', start=0, end=2 * np.pi, value=default_phase, step=0.05)
s_noise_mean = Slider(title='Амплітуда шуму', start=-1.0, end=1.0, value=default_noise_mean, step=0.05)
s_noise_covariance = Slider(title='Дисперсія шуму', start=0.0, end=1.0, value=default_noise_covariance, step=0.05)
s_cutoff_frequency = Slider(title='Частота зрізу', start=0.1, end=20.0, value=default_cutoff_frequency, step=0.05)
s_filter_order = Slider(title='Порядок фільтру', start=1, end=10, value=default_filter_order, step=1)

check_show_noise = Toggle(label="Показати шум", button_type="success")

reset_button = Button(label="Скинути", button_type="warning")
reset_button.on_click(reset_values)

# Додаємо обробники подій для оновлення графіків та параметрів
widgets = (s_amplitude, s_frequency, s_phase, s_cutoff_frequency, s_filter_order)
for widget in widgets:
    widget.on_change('value', update_plot)

s_noise_mean.on_change('value', update_noise)
s_noise_covariance.on_change('value', update_noise)

check_show_noise.on_change("active", update_plot)

# Set up layouts and add to document
inputs = column(*widgets, s_noise_mean, s_noise_covariance, check_show_noise, reset_button)
update_plot(None, None, None)

# Додаємо графік та елементи інтерфейсу до документа Bokeh
curdoc().title = "Zpad"
curdoc().add_root(row(plot, inputs, width=1200))
