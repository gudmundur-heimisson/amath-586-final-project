import matplotlib.pyplot as plt
import numpy as np

def celsius2kelvin(celsius):
    return celsius + 273.15

def kelvin2celsius(kelvin):
    return kelvin - 273.15

def thermal_conductivity(water_content, porosity):
    a = 6.45e-1
    b = 6.34e-1
    l = 3e-2
    X = water_content
    e = porosity
    q = a * X / (1 + X) + b
    return q * ((1 - e) * (2 * q + l) + 3 * e * l) / ((1 - e) * (2 * q + l) + 3 * e * q)

def diffusivity(water_content, temperature):
    X = water_content
    T = temperature
    c = 3.28e-5
    d = 5.25e-6
    e = 22261.7
    R = 8.3144598
    return (c * X + d) * np.exp(-e / (R * T))



if __name__ == '__main__':
    porosities = np.linspace(0.2, 0.6, 5, endpoint=True)
    water_content = np.linspace(0.05, 0.4, 200)
    for porosity in porosities:
        plt.plot(water_content, thermal_conductivity(water_content, porosity), label=porosity)
    plt.legend()
    plt.show()
    temperatures = np.linspace(celsius2kelvin(25), celsius2kelvin(200), 20)
    for temperature in temperatures:
        plt.plot(water_content, diffusivity(water_content, temperature), label=kelvin2celsius(temperature))
    plt.legend()
    plt.show()
