# Author: Guðmundur Heimisson
# Email: heimig@uw.edu
# AMATH 586 Final Project Code
# main module

import matplotlib.pyplot as plt
import numpy as np
from ode.properties import batter_thermal_conductivity, batter_water_diffusivity, \
    atmospheric_pressure, batter_vapor_content, batter_air_content, \
    batter_heat_capacity, batter_density, \
    partial_vapor_pressure, batter_thermal_diffusivity
from ode.crank_nicholson import CrankNicholsonSolver
from ode.scaling import scale2temperature, scale2time, scale2displacement

def celsius2kelvin(celsius):
    return celsius + 273.15

def kelvin2celsius(kelvin):
    return kelvin - 273.15

def generate_thermal_conductivity_graph():
    porosity = np.linspace(0.06, 0.56, 200)
    water_content = np.linspace(0.1, 0.4, 200)
    X, e = np.meshgrid(water_content, porosity)
    tc = batter_thermal_conductivity(X, e)
    CS = plt.contourf(X, e, tc, 100)
    plt.title(r'Thermal conductivity $\lambda$ of batter ($\mathrm{W\,m^{-1}\,K^{-1}}$)')
    plt.xlabel(r'Water content $X$ (kg/kg)')
    plt.ylabel(r'Porosity $\varepsilon$ ($-$)')
    plt.colorbar(CS)
    plt.show()

def generate_water_content_graph():
    water_content = np.linspace(0.1, 0.4, 200)
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    X, T = np.meshgrid(water_content, temperature)
    wd = batter_water_diffusivity(X, T)
    CS = plt.contourf(X, kelvin2celsius(T), wd, 100)
    plt.title(r'Liquid water diffusivity $D_l$ ($\mathrm{m^2\,s^{-1}}$)')
    plt.xlabel(r'Water content $X$ (kg/kg)')
    plt.ylabel(r'Temperature $T$ (°C)')
    plt.colorbar(CS)
    plt.show()

def generate_thermal_diffusivity_graph():
    water_content = np.linspace(0.1, 0.4, 200)
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    e = 0.5
    X, T = np.meshgrid(water_content, temperature)
    P = atmospheric_pressure
    K = batter_thermal_diffusivity(X, T, P, e)
    CS = plt.contourf(X, kelvin2celsius(T), K, 100)
    plt.title(r'Thermal diffusivity $\kappa$ of batter at $P_{\mathrm{atm}}$ ($\mathrm{m^2\,s^{-1}}$)')
    plt.xlabel(r'Water content $X$ (kg/kg)')
    plt.ylabel(r'Temperature $T$ (°C)')
    plt.colorbar(CS)
    plt.show()

def generate_batter_heat_capacity_graph():
    water_content = np.linspace(0.1, 0.4, 200)
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    X, T = np.meshgrid(water_content, temperature)
    e = 0.5
    P = atmospheric_pressure
    hc = batter_heat_capacity(X, T, P)
    CS = plt.contourf(X, kelvin2celsius(T), hc, 100)
    plt.colorbar(CS)
    plt.show()

def generate_batter_air_content_graph():
    X = 0.3
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    pressure = np.linspace(atmospheric_pressure/2, atmospheric_pressure, 200)
    T, P = np.meshgrid(temperature, pressure)
    CS = plt.contourf(kelvin2celsius(T), P, batter_air_content(X, T, P), 100)
    plt.colorbar(CS)
    plt.show()

def generate_batter_vapor_content_graph():
    water_content = np.linspace(0.1, 0.4, 200)
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    X, T = np.meshgrid(water_content, temperature)
    CS = plt.contourf(X, kelvin2celsius(T), batter_vapor_content(X, T), 100)
    plt.colorbar(CS)
    plt.show()

def generate_partial_vapor_pressure_graph():
    water_content = np.linspace(0.1, 0.4, 200)
    temperature = celsius2kelvin(np.linspace(20, 80, 200))
    X, T = np.meshgrid(water_content, temperature)
    CS = plt.contourf(X, kelvin2celsius(T), partial_vapor_pressure(X, T), 100)
    plt.colorbar(CS)
    plt.show()

def generate_temperature_distribution_graph():
    start_grid = 0
    end_grid = 1
    grid_size = 500
    timestep = 0.01
    grid = np.linspace(start_grid, end_grid, grid_size+2, endpoint=True)
    initial_state = np.array((grid_size+2) * [0.0])
    left_flux = 0
    right_flux = 2.03e11
    solver = CrankNicholsonSolver(initial_state, left_flux, right_flux, timestep,
                                  grid_size,
                                  start_grid=start_grid, end_grid=end_grid,
                                  end_time=1)
    for t, u in solver:
        if np.abs((10 * (t % 1)) % 1)  <= 0.0001:
            plt.plot(grid, u, '-', label=t)
    plt.legend()
    plt.show()

def generate_temperature_slices_graph():
    start_grid = 0
    end_grid = 1
    grid_size = 500
    timestep = 0.001
    grid = np.linspace(start_grid, end_grid, grid_size+2, endpoint=True)
    initial_state = np.array((grid_size+2) * [0.0])
    left_flux = 0
    right_flux = 2.03e11
    solver = CrankNicholsonSolver(initial_state, left_flux, right_flux, timestep, 
                                  grid_size,
                                  start_grid=start_grid, end_grid=end_grid,
                                  end_time=0.3)
    slice_indices = [1, round(grid_size / 4), round(grid_size/2),
                     round(3*grid_size/4), round(0.99 * grid_size)]
    times = []
    slice_data = [[], [], [], [], []]
    print(slice_indices)
    for t, u in solver:
        times.append(t)
        for i, index in enumerate(slice_indices):
            slice_data[i].append(u[index])
    for i, data in enumerate(slice_data):
        x = scale2displacement(grid[slice_indices[i]])
        plt.plot(scale2time(np.array(times)), 
                kelvin2celsius(scale2temperature(np.array(data))),
                label='{:0.3f} $\\mathrm{{m}}$'.format(x))
    plt.title(r'Temperature profiles for selected depth slices')
    plt.xlabel(r'Time $t$ (s)')
    plt.ylabel(r'Temperature $T$ (°C)')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    generate_thermal_conductivity_graph()
    generate_water_content_graph()
    generate_thermal_diffusivity_graph()
    generate_batter_air_content_graph()
    generate_batter_vapor_content_graph()
    generate_partial_vapor_pressure_graph()
    generate_batter_heat_capacity_graph()
    generate_temperature_slices_graph()