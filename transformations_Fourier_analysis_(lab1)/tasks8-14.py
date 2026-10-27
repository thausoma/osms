import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


print("Задание 9 и 10")
y, fs = sf.read('data/voice.wav')

print(f"Количество сэмплов и дорожек: f{y.shape}\nФормат представления амплитуды: {y.dtype}\nЧастота дискретизации: {fs}")
print(f"Количество сэмплов (2 способ): {len(y)}\nДлительность записи: {len(y)/fs}")
print(f"Диапазон амплитуд {y.min(), y.max()}")


print("\n\n\nЗадание 11")

y1 = y[::10] # прореживание
fs1 = fs / 10  # новая ч.д.

print(f"Оригинал: {len(y)} отсчётов, fs = {fs} Гц")
print(f"Прореженный: {len(y1)} отсчётов, fs1 = {fs1} Гц")

print("нормальный сигнал")
sd.play(y, fs)
sd.wait()
print("прореженный сигнал")
sd.play(y1, fs1)
sd.wait()

plt.figure(figsize=(12, 4))
plt.plot(y1)
plt.xlabel('Номер отсчёта')
plt.ylabel('Амплитуда')
plt.title(f'Прореженный сигнал (fs1 = {fs1} Гц)')
plt.grid(True)
plt.show()


print("\n\n\nЗадание 12")

Y_orig = np.fft.rfft(y) # спектр оригинального сигнала
freqs_orig = np.fft.rfftfreq(len(y), d=1/fs)

Y_dec = np.fft.rfft(y1) # спектр прореженного сигнала
freqs_dec = np.fft.rfftfreq(len(y1), d=1/fs1)

plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
plt.plot(freqs_orig, np.abs(Y_orig) / len(y))
plt.title(f'Спектр оригинала (fs = {fs} Гц)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.xlim(0, fs/2)
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(freqs_dec, np.abs(Y_dec) / len(y1))
plt.title(f'Спектр прореженного (fs1 = {fs1} Гц)')
plt.xlabel('Частота, Гц')
plt.ylabel('Амплитуда')
plt.xlim(0, fs1/2)
plt.grid(True)
plt.tight_layout()
plt.show()


import numpy as np
import matplotlib.pyplot as plt

print("Задание 13")

frequency = 26
period = 1/frequency
t = np.linspace(0, 1.0, num=10000)

y = 4*np.cos(2*np.pi*frequency*t + np.pi/12)

floor = round(np.min(y), 6)
ceil = round(np.max(y), 6)

print("Минимальное значение функции: ", floor)
print("Максимальное значение функции: ", ceil)

Powers = [3, 4, 5, 6]

plt.figure(figsize=(14, 10))

for idx, power in enumerate(Powers):
    L = 2**power
    delta = (ceil - floor)/L
    diapason = []
    for i in range(0, L):
        diapason.append(floor + delta*i)
    indices = np.round((y - floor) / delta) # ампл. сигнала от -4 до 4 --> от 0 до 8
    indices = np.clip(indices, 0, L - 1) # клиппинг
    y_quantized = indices * delta + floor
    

    error = np.mean(np.abs(y - y_quantized)) # средняя ошибка
    print(f"Разрядность АЦП: {power} бит\nУровней: {L}\nШаг квантования: {delta}\nСредняя ошибка: {error}")
    

    Y_q = np.fft.rfft(y_quantized) # спектр квантованного сигнаба
    freqs_q = np.fft.rfftfreq(len(y_quantized), d=(t[1]-t[0])) 
    

    plt.subplot(2, 2, idx + 1)
    plt.plot(freqs_q, np.abs(Y_q) / len(y_quantized))
    plt.title(f'Спектр при {power} битах (Ошибка: {error:.5f})')
    plt.xlabel('Частота, Гц')
    plt.ylabel('Амплитуда')
    plt.xlim(0, 100)
    plt.grid(True)

plt.tight_layout()
plt.show()