# Author: Guðmundur Heimisson
# Email: heimig@uw.edu
# AMATH 586 Final Project Code
# module ode.properties
import numpy as np

gas_constant = 8.3144598
batter_density = 880
solid_heat_capacity = 1.9518e3
thermal_conductivity_air = 2.8e-2
air_heat_capacity = 1.01e3
water_heat_capacity = 4.1796e3
vapor_heat_capacity = 1.840e3
atmospheric_pressure = 1.01325e5
air_molar_mass = 2.8964e-2
vapor_molar_mass = 1.8016e-2
air_kinematic_viscosity = 1.87e-5
vapor_kinematic_viscosity = 2.0339e-5
water_vaporization_enthalpy = 4.065e3


def batter_thermal_conductivity(water_content, porosity):
    a = 6.45e-1
    b = 1.34e-1
    X = water_content
    e = porosity
    l = thermal_conductivity_air
    Q = a * X / (1 + X) + b
    P = (1 - e) * (2 * Q + l)
    return Q * (P + 3 * e * l) / (P + 3 * e * Q)

def batter_water_diffusivity(water_content, temperature):
    c = 3.28e-5
    d = 5.25e-6
    E = 2.22617e4
    X = water_content
    T = temperature
    R = gas_constant
    return (c * X + d) * np.exp(-E / (R * T))

def batter_water_activity(water_content):
    return np.exp(-2.95 / np.power(100 * water_content, 0.78))

def pure_partial_vapor_pressure(temperature):
    T = temperature
    return (6.1121e-4) * np.exp((18.678 - (273.15 + T) / 234.5) * ((273.15 + T) / (530.20 + T)))

def partial_vapor_pressure(water_content, temperature):
    return batter_water_activity(water_content) * pure_partial_vapor_pressure(temperature)

def batter_vapor_content(water_content, temperature):
    return (vapor_molar_mass * partial_vapor_pressure(water_content, temperature)) / (batter_density * gas_constant * temperature)

def batter_air_content(water_content, temperature, pressure):
    p = pressure - partial_vapor_pressure(water_content, temperature)
    return (air_molar_mass * p) / (batter_density * gas_constant * temperature)

def humid_air_molar_mass(vapor_content, air_content):
    vapor_moles = vapor_content / vapor_molar_mass
    air_moles = air_content / air_molar_mass
    return (vapor_moles * vapor_molar_mass + air_moles * air_molar_mass) / (vapor_moles + air_moles)

def humid_air_heat_capacity(vapor_content, air_content):
    vapor_moles = vapor_content / vapor_molar_mass
    air_moles = air_content / air_molar_mass
    return (vapor_moles * vapor_heat_capacity + air_moles * air_heat_capacity) / (vapor_moles + air_moles)

def humid_air_kinematic_viscosity(vapor_content, air_content):
    vapor_moles = vapor_content / vapor_molar_mass
    air_moles = air_content / air_molar_mass
    return (vapor_moles * vapor_kinematic_viscosity + air_moles * air_kinematic_viscosity) / (vapor_moles + air_moles)

def batter_heat_capacity(water_content, temperature, pressure):
    vapor_content = batter_vapor_content(water_content, temperature)
    air_content = batter_air_content(water_content, temperature, pressure)
    solid_content = 1 - water_content
    humid_air_content = vapor_content + air_content
    return solid_content * solid_heat_capacity + water_content * water_heat_capacity + humid_air_content * humid_air_heat_capacity(vapor_content, air_content)

def batter_thermal_diffusivity(water_content, temperature, pressure, porosity):
    heat_capacity = batter_heat_capacity(water_content, temperature, pressure)
    tc = batter_thermal_conductivity(water_content, porosity)
    return tc / (batter_density * (1 - porosity) * heat_capacity)
