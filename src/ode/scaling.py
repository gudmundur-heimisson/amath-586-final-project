def scale2temperature(scale):
    return 180.0 * scale + 293.15

def scale2time(scale):
    return 1.35e4 * scale

def scale2displacement(scale):
    return 0.04 * scale