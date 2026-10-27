import numpy as np
import matplotlib.pyplot as plt


TxPower_BS = 46.0
TxPower_UE = 24.0
AntGain_BS = 21.0
PenetrationM = 15.0
IM = 1.0
sectors_per_BS = 3
f_MHz = 1800.0
f_GHz = f_MHz / 1000.0
BW_UL = 10e6
BW_DL = 20e6
NoiseFigure_BS = 2.4
NoiseFigure_UE = 6.0
RequiredSINR_UL = 4.0
RequiredSINR_DL = 2.0
mimo_antennas_BS = 2
area_macro = 100.0
area_femto = 4.0

feeder_loss = 2.0
lna_loss = 0.4
jumper_loss = 0.5
FeederLoss = feeder_loss + lna_loss + jumper_loss
MIMOGain = 10 * np.log10(mimo_antennas_BS)

h_BS = 50.0 # 30-200m
h_ms = 1.8 # 1-10m
clutter = 'U'

building_height = 20.0 # WI
street_width = 20.0
building_spacing = 30.0
street_angle = 70.0

A_TABLE = {'150-1500': 69.55, '1500-2000': 46.3}
B_TABLE = {'150-1500': 26.16, '1500-2000': 33.9}
frequency_band = '1500-2000'

ThermalNoise_UL = -174 + 10 * np.log10(BW_UL)
ThermalNoise_DL = -174 + 10 * np.log10(BW_DL)

RxSens_BS = NoiseFigure_BS + ThermalNoise_UL + RequiredSINR_UL
RxSens_UE = NoiseFigure_UE + ThermalNoise_DL + RequiredSINR_DL

MAPL_UL = (TxPower_UE - FeederLoss + AntGain_BS + MIMOGain - IM - PenetrationM - RxSens_BS) # ф. 2.20
MAPL_DL = (TxPower_BS - FeederLoss + AntGain_BS + MIMOGain - IM - PenetrationM - RxSens_UE) # ф. 2.19

def uminlos_pathloss(distance_km): # ф. 2.3
    distance_m = distance_km * 1000.0
    return 26 * np.log10(f_GHz) + 22.7 + 36.7 * np.log10(distance_m)

def hata_coeff_a(ms_height): # ф. 2.5
    if clutter in ('DU', 'U'):
        return 3.2 * np.log10(11.75 * ms_height) ** 2 - 4.97
    return (1.1 * np.log10(f_MHz)) * ms_height - (1.56 * np.log10(f_MHz) - 0.8)

def L_clutter(): # ф. 2.6
    if clutter == 'DU':
        return 3.0
    if clutter == 'U':
        return 0.0
    if clutter == 'SU':
        return -(2 * np.log10(f_MHz / 28) ** 2 + 5.4)
    if clutter == 'RURAL':
        return -(4.78 * np.log10(f_MHz) ** 2 - 18.33 * np.log10(f_MHz) + 40.94)
    return -(4.78 * np.log10(f_MHz) ** 2 - 18.33 * np.log10(f_MHz) + 35.94)

def hata_distance_slope(distance_km): # ф. 2.7
    slope_far = 44.9 - 6.55 * np.log10(f_MHz)
    slope_near = ((47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(h_BS))/ np.log10(50))
    return np.where(distance_km >= 1.0, slope_far, slope_near)

def cost231_hata_pathloss(distance_km): # ф. 2.4
    A = A_TABLE[frequency_band]
    B = B_TABLE[frequency_band]
    return (A + B * np.log10(f_MHz) - 13.82 * np.log10(h_BS) - hata_coeff_a(h_ms) + hata_distance_slope(distance_km) * np.log10(distance_km) + L_clutter())

def walfish_ikegami_los_loss(distance_km): # ф. 2.8
    return 42.6 + 20 * np.log10(f_MHz) + 26 * np.log10(distance_km)

def walfish_ikegami_nlos_loss(distance_km): # ф. 2.9-16
    L0 = 32.44 + 20 * np.log10(f_MHz) + 20 * np.log10(distance_km)  # ф. 2.10

    roof_over_mobile = building_height - h_ms
    bs_over_roof = h_BS - building_height
    phi_term = np.where(street_angle < 35, -10 + 0.354 * street_angle, np.where(street_angle < 55, 2.5 + 0.075 * street_angle, 4.0 - 0.114 * street_angle)) # ф. 2.11

    L2 = (-16.9 - 10 * np.log10(street_width) + 10 * np.log10(f_MHz) + 20 * np.log10(roof_over_mobile) + phi_term)

    L11 = np.where(bs_over_roof > 0, -18 * np.log10(1 + bs_over_roof), 0.0) # ф. 2.13
    ka = np.where(bs_over_roof > 0, 54.0, np.where(distance_km > 0.5, 54 - 0.8 * bs_over_roof, 54 - 0.8 * bs_over_roof * distance_km / 0.5)) # ф. 2.14
    kd = np.where(bs_over_roof > 0, 18.0, 18 - 15 * bs_over_roof / building_height) # ф. 2.15
    kf = -4 + 0.7 * (f_MHz / 925 - 1) # ф. 2.16

    L1 = (L11 + ka + kd * np.log10(distance_km) + kf * np.log10(f_MHz) - 9 * np.log10(building_spacing)) # ф. 2.12
    return L0 + np.maximum(L1 + L2, 0.0) # ф. 2.9



distance_grid = np.logspace(np.log10(0.03), np.log10(20), 2000)

def find_radius(loss_function, mapl):
    loss_curve = loss_function(distance_grid)
    return np.interp(mapl, loss_curve, distance_grid)

radius_UL_macro = find_radius(cost231_hata_pathloss, MAPL_UL)
radius_DL_macro = find_radius(cost231_hata_pathloss, MAPL_DL)
radius_UL_femto = find_radius(uminlos_pathloss, MAPL_UL)
radius_DL_femto = find_radius(uminlos_pathloss, MAPL_DL)



sector_factor = {2: 1.73, 3: 1.95, 6: 2.6}

radius_macro = min(radius_UL_macro, radius_DL_macro)
radius_femto = min(radius_UL_femto, radius_DL_femto)

site_area_macro = sector_factor[sectors_per_BS] * radius_macro ** 2
site_area_femto = sector_factor[sectors_per_BS] * radius_femto ** 2

bs_count_macro = int(np.ceil(area_macro / site_area_macro))
bs_count_femto = int(np.ceil(area_femto / site_area_femto))


print(f'ThermalNoise UL / DL: {ThermalNoise_UL:.2f} / {ThermalNoise_DL:.2f} дБм')
print(f'RxSens BS / UE:       {RxSens_BS:.2f} / {RxSens_UE:.2f} дБм')
print(f'FeederLoss: {FeederLoss:.1f} дБ, MIMOGain: {MIMOGain:.2f} дБ')
print(f'MAPL_UL: {MAPL_UL:.2f} дБ, MAPL_DL: {MAPL_DL:.2f} дБ')
print()
print(f'Макросоты (COST231 Hata): d_UL = {radius_UL_macro:.2f} км, ' f'd_DL = {radius_DL_macro:.2f} км, радиус = {radius_macro:.2f} км')
print(f'  площадь сайта = {site_area_macro:.2f} кв.км, БС нужно = {bs_count_macro}')
print(f'Фемто/микросоты (UMiNLOS): d_UL = {radius_UL_femto:.3f} км, ' f'd_DL = {radius_DL_femto:.3f} км, радиус = {radius_femto:.3f} км')
print(f'  площадь сайта = {site_area_femto:.3f} кв.км, БС нужно = {bs_count_femto}')

plt.figure(figsize=(11, 6))
plt.plot(distance_grid, cost231_hata_pathloss(distance_grid), label='COST231 Hata')
plt.plot(distance_grid, uminlos_pathloss(distance_grid), label='UMiNLOS')
plt.plot(distance_grid, walfish_ikegami_nlos_loss(distance_grid), label='Walfish-Ikegami NLOS')
plt.plot(distance_grid, walfish_ikegami_los_loss(distance_grid), '--', label='Walfish-Ikegami LOS')
plt.axhline(MAPL_UL, color='green', lw=1, label=f'MAPL_UL = {MAPL_UL:.1f} дБ')
plt.axhline(MAPL_DL, color='red', lw=1, label=f'MAPL_DL = {MAPL_DL:.1f} дБ')
plt.xlim(0, 10)
plt.xlabel('Расстояние d, км')
plt.ylabel('Потери PL(d), дБ')
plt.title('Сравнение моделей распространения (п.3 задания)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.figure(figsize=(11, 6))
plt.plot(distance_grid, cost231_hata_pathloss(distance_grid), label='COST231 Hata')
plt.axhline(MAPL_UL, color='green', lw=1)
plt.axhline(MAPL_DL, color='red', lw=1)
plt.plot(radius_UL_macro, MAPL_UL, 'go')
plt.plot(radius_DL_macro, MAPL_DL, 'ro')
plt.annotate(f'd_UL = {radius_UL_macro:.2f} км', (radius_UL_macro, MAPL_UL), textcoords='offset points', xytext=(10, -12))
plt.annotate(f'd_DL = {radius_DL_macro:.2f} км', (radius_DL_macro, MAPL_DL), textcoords='offset points', xytext=(10, -12))
plt.xlim(0, 5)
plt.xlabel('Расстояние d, км')
plt.ylabel('Потери PL(d), дБ')
plt.title('Макросоты: радиусы UL и DL (рис. 2.6)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.figure(figsize=(11, 6))
plt.plot(distance_grid, uminlos_pathloss(distance_grid), label='UMiNLOS')
plt.axhline(MAPL_UL, color='green', lw=1)
plt.axhline(MAPL_DL, color='red', lw=1)
plt.plot(radius_UL_femto, MAPL_UL, 'go')
plt.plot(radius_DL_femto, MAPL_DL, 'ro')
plt.annotate(f'd_UL = {radius_UL_femto:.3f} км', (radius_UL_femto, MAPL_UL), textcoords='offset points', xytext=(10, -12))
plt.annotate(f'd_DL = {radius_DL_femto:.3f} км', (radius_DL_femto, MAPL_DL), textcoords='offset points', xytext=(10, -12))
plt.xlim(0, 2)
plt.xlabel('Расстояние d, км')
plt.ylabel('Потери PL(d), дБ')
plt.title('Фемто/микросоты: радиусы UL и DL (рис. 2.6)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()