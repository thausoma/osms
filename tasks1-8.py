#вариант 25
import numpy as np
import matplotlib.pyplot as plt


print("Задание 1")

frequency = 26
period = 1/frequency
phase = 0
A_t = 0
t = np.linspace(0, 5*period, num=10000) # сигнал должен быть непрерывным, поэтому чтобы это имитировать я поставил большой num.

A_t = 4*np.cos(2*np.pi*frequency*t + np.pi/12)

plt.xlabel("Время, t")
plt.ylabel("Амплитуда, A")

plt.plot(t, A_t)
plt.grid()
plt.show() 
 

print("Задание 2")

print(f"Максимальная частота в спектре данной функции = {frequency} Гц. \nА если бы гармонических функций было бы несколько в сумме, \nнужно было бы взять частоту той из них, максимальная относительно остальных")


print("Задание 3")

sampling_frequency_min = frequency*2 + 1

print(f"По т. Котельникова, ч. дискретизации > 2 * ч. колебания. Минимально необходимая ч.д.:  {sampling_frequency_min} Гц")


print("Задание 4")

sample_moments = []
sample_values = []

for i in np.arange(0, 1.0, 1/sampling_frequency_min):
    sample_moments.append(i)
    sample_values.append(float(4*np.cos(2*np.pi*frequency*i + np.pi/12)))

plt.xlabel("Время, t")
plt.ylabel("Амплитуда, A")
plt.stem(sample_moments, sample_values)
plt.grid()
plt.show() 
print("p.s. на графике бантик, однако дискретизация выполнена правильно. если вместо 1.0 в arange поставить 5*period, а к sampling_frequency_min прибавить не 1, а 1000, то получится ожидаемый дискретизированный сигнал.")


print("Задание 5")

F_x = []
F_x_reals = []
harmonics_freqs = []
N = len(sample_moments)

for x in range(0, N):
    harmonics_freqs.append((x*sampling_frequency_min)/N)
    sum_val = 0
    for n in range(0, N):
        sum_val += sample_values[n] * np.exp(-1j*2*np.pi*(x*(n/N)))
    F_x.append(sum_val)

for i in range (len(F_x)):
    F_x_reals.append(abs(F_x[i])/N) # деление на N - это НОРМИРОВКА! без неё амплитуда улетает за 400

if len(F_x_reals) != len(sample_moments):
    print("warning количество отсчётов не совпадает с количеством сэмплов")

plt.xlabel("Частота")
plt.ylabel("Амплитуда, A")
plt.stem(harmonics_freqs, F_x_reals)
plt.grid()
plt.show() 


print("Задание 6")

t_fine = np.linspace(0, 1, 10000)
A_fine = 4*np.cos(2*np.pi*frequency*t_fine + np.pi/12)

plt.xlabel("Время, t")
plt.ylabel("Амплитуда, A")
plt.plot(t_fine, A_fine, label='Оригинальный сигнал', color='red')
plt.plot(sample_moments, sample_values, '-o', label='Восстановленный сигнал', color='blue')
plt.grid()
plt.show() 
print('Сходство не очень хорошее. это из - за того, что частота дискретизации довольно небольшая, но АЦП этого было бы достаточно')


print('Задание 7')

sampling_frequency_opt = sampling_frequency_min*4

sample_moments = []
sample_values = []

for i in np.arange(0, 1.0, 1/sampling_frequency_opt):
    sample_moments.append(i)
    sample_values.append(float(4*np.cos(2*np.pi*frequency*i + np.pi/12)))

F_x = []
F_x_reals = []
harmonics_freqs = []
N = len(sample_moments)

for x in range(0, N):
    harmonics_freqs.append((x*sampling_frequency_opt)/N)
    sum_val = 0
    for n in range(0, N):
        sum_val += sample_values[n] * np.exp(-1j*2*np.pi*(x*(n/N)))
    F_x.append(sum_val)

for i in range (len(F_x)):
    F_x_reals.append(abs(F_x[i])/N)

if len(F_x_reals) != len(sample_moments):
    print("warning количество отсчётов не совпадает с количеством сэмплов")

plt.xlabel("Частота")
plt.ylabel("Амплитуда, A")
plt.stem(harmonics_freqs, F_x_reals)
plt.grid()
plt.show() 

plt.xlabel("Время, t")
plt.ylabel("Амплитуда, A")
plt.plot(t_fine, A_fine, label='Оригинальный сигнал', color='red')
plt.plot(sample_moments, sample_values, '-o', label='Восстановленный сигнал', color='blue')
plt.grid()
plt.show() 
print('Сходство значительно лучше.')

