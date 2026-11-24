from pygame import *   
import sounddevice as sd 
from scipy.io.wavfile import wav

# === Налаштування ===
fs = 44100     # Частота дискретизації (кількість вимірів за секунду)
chunk = 1024   # Кількість семплів (відліків) за один кадр
width, height = 800, 400  

recording = None
is_recording = False
voice_file = "voice.wav"
minus_track = "MinusDuHast.mp3"

init()
screen = display.set_mode((width, height))
display.set_caption("Live Audio (Mic)")
clock = time.Clock()

font.init()
font_big = font.SysFont("Arial", 35)

btn_rect = Rect(425, 280, 250, 80)
rect_color = "white"
btn_text = "Record"

# Початкові дані — масив нулів (ще немає звуку)
data = [0.0] * chunk

# === Функція, яку викликає sounddevice, коли приходить нова порція звуку ===
def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)  # Якщо є помилки або попередження, виводимо їх
    # Перетворюємо отриманий звук у список і масштабуємо під висоту екрану
    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]

# === Запуск потоку з мікрофона ===
stream = sd.InputStream(
    callback=audio_callback,  # Функція для отримання аудіо
    channels=1,               # Один канал (моно)
    samplerate=fs,             # Частота дискретизації
    blocksize=chunk,           # Розмір буфера (chunk)
    dtype='float32'            # Тип даних (числа з плаваючою комою)
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Готуємо список точок для малювання хвилі
    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)          # Позиція X для точки
        y = int(height / 2 + sample)        # Позиція Y для точки
        points.append((x, y))               # Додаємо точку в список

    # Малюємо лінію по точках, якщо їх більше однієї
    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    display.update()
    clock.tick(60)

stream.stop()
quit()

