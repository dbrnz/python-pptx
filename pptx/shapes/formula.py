import math


PRESET_GUIDES = {}

PRESET_GUIDES['3cd4']   = 16200000.0       # 3/4 of a Circle
PRESET_GUIDES['3cd8']   =  8100000.0       # 3/8 of a Circle
PRESET_GUIDES['5cd8']   = 13500000.0       # 5/8 of a Circle
PRESET_GUIDES['7cd8']   = 18900000.0       # 7/8 of a Circle
PRESET_GUIDES['cd2']    = 10800000.0       # 1/2 of a Circle
PRESET_GUIDES['cd4']    =  5400000.0       # 1/4 of a Circle
PRESET_GUIDES['cd8']    =  2700000.0       # 1/8 of a Circle

PRESET_GUIDES['t']      = 0                # Shape Top Edge
PRESET_GUIDES['b']      = 'val h'          # Shape Bottom Edge
PRESET_GUIDES['vc']     = '*/ h 1.0 2.0'   # Vertical Center of Shape
PRESET_GUIDES['hd2']    = '*/ h 1.0 2.0'   # 1/2 of Shape Height
PRESET_GUIDES['hd3']    = '*/ h 1.0 3.0'   # 1/3 of Shape Height
PRESET_GUIDES['hd4']    = '*/ h 1.0 4.0'   # 1/4 of Shape Height
PRESET_GUIDES['hd5']    = '*/ h 1.0 5.0'   # 1/5 of Shape Height
PRESET_GUIDES['hd6']    = '*/ h 1.0 6.0'   # 1/6 of Shape Height
PRESET_GUIDES['hd8']    = '*/ h 1.0 8.0'   # 1/8 of Shape Height

PRESET_GUIDES['l']     = 0                 # Shape Left Edge
PRESET_GUIDES['r']     = 'val w'           # Shape Right Edge
PRESET_GUIDES['hc']    = '*/ w 1.0 2.0'    # Horizontal Center
PRESET_GUIDES['wd2']   = '*/ w 1.0 2.0'    # 1/2 of Shape Width
PRESET_GUIDES['wd3']   = '*/ w 1.0 3.0'    # 1/3 of Shape Width
PRESET_GUIDES['wd4']   = '*/ w 1.0 4.0'    # 1/4 of Shape Width
PRESET_GUIDES['wd5']   = '*/ w 1.0 5.0'    # 1/5 of Shape Width
PRESET_GUIDES['wd6']   = '*/ w 1.0 6.0'    # 1/6 of Shape Width
PRESET_GUIDES['wd8']   = '*/ w 1.0 8.0'    # 1/8 of Shape Width
PRESET_GUIDES['wd10']  = '*/ w 1.0 10.0'   # 1/10 of Shape Width

PRESET_GUIDES['ls']    = 'max w h'         # Longest Side of Shape
PRESET_GUIDES['ss']    = 'min w h'         # Shortest Side of Shape
PRESET_GUIDES['ssd2']  = '*/ ss 1.0 2.0'   # 1/2 Shortest Side of Shape
PRESET_GUIDES['ssd4']  = '*/ ss 1.0 4.0'   # 1/4 Shortest Side of Shape
PRESET_GUIDES['ssd6']  = '*/ ss 1.0 6.0'   # 1/6 Shortest Side of Shape
PRESET_GUIDES['ssd8']  = '*/ ss 1.0 8.0'   # 1/8 Shortest Side of Shape
PRESET_GUIDES['ssd16'] = '*/ ss 1.0 16.0'  # 1/16 Shortest Side of Shape
PRESET_GUIDES['ssd32'] = '*/ ss 1.0 32.0'  # 1/32 Shortest Side of Shape


STANGLE_PER_DEGREE = 60000

variables = {
    'w': 20,  # The variable width of the shape defined in the shape properties. This value is received from the shape transform listed within the <spPr> element.
    'h': 30,  # The variable height of the shape defined in the shape properties. This value is received from the shape transform listed within the <spPr> element.
}



'''
Guides evaluated in order

class Guide(object):
    def __init__(self, name, fmla):
        pass

    def value(self):
        pass

class GuideList(object):
    def __init__(self):
        self._guides = {}
'''

def value(x):
    try: return float(x)
    except ValueError: pass
    try: return value(PRESET_GUIDES[x])
    except KeyError: pass
    try: return value(variables[x])
    except KeyError: pass
    return Evaluator.evaluate(x)


def radians(x):
    return value(x)*math.pi/(STANGLE_PER_DEGREE*180)

def st_angle(x):
    return x*STANGLE_PER_DEGREE*180/math.pi


class Evaluator(object):

    formulae = {
        '*/': lambda x, y, z: value(x)*value(y)/value(z),              # Multiply Divide Formula
        '+-': lambda x, y, z: value(x) + value(y) - value(z),          # Add Subtract Formula
        '+/': lambda x, y, z: (value(x) + value(y))/value(z),          # Add Divide Formula
        '?:': lambda x, y, z: value(y) if value(x) > 0 else value(z),  # If Else Formula

        'at2': lambda x, y: (st_angle(math.atan(value(y)/value(x))) if value(x) != 0.0   # ArcTan Formula
                        else value('cd4' if value(y) >= 0 else '3cd4')),
        'tan': lambda x, y: value(x)*math.tan(radians(y)),             # Tangent Formula
        'cat2': lambda x, y, z: (value(x)*math.cos(math.atan(value(z)/value(y))) if value(y) != 0.0    # Cosine ArcTan Formula
                            else 0.0),
        'cos': lambda x, y: value(x)*math.cos(radians(y)),             # Cosine Formula
        'sat2': lambda x, y, z: (value(x)*math.sin(math.atan(value(z)/value(y))) if value(y) != 0.0   # Sine ArcTan Formula
                           else  value(x) if value(z) >= 0
                           else -value(x)),
        'sin': lambda x, y: value(x)*math.sin(radians(y)),             # Sine Formula

        'mod': lambda x, y, z: math.sqrt(value(x)**2 + value(y)**2 + value(z)**2), # Modulo Formula
        'sqrt': lambda x: math.sqrt(value(x)),                         # Square Root Formula

        'val': lambda x: value(x),                                     # Literal Value Formula
        'abs': lambda x: abs(value(x)),                                # Absolute Value Formula
        'max': lambda x, y: max(value(x), value(y)),                   # Maximum Value Formula
        'min': lambda x, y: min(value(x), value(y)),                   # Minimum Value Formula
        'pin': lambda x, y, z: (value(x) if value(y) < value(x)        # Pin To Formula
                           else value(z) if value(y) > value(z)
                           else value(y)),
    }

    @staticmethod
    def evaluate(expr):
        args = expr.split()
        return Evaluator.formulae[args[0]](*args[1:])


if __name__ == '__main__':
    variables['x'] = '*/ 1 2 3'
    print(value('val x'))
    print(value('wd10'))
    print(value('cos 1 0'))
    print(value('at2 0 1'))
    print(value('cat2 1 0 1'))
    print(value('cat2 1 1 1'))
    print(value('sat2 1 1 1'))
    print(value('sat2 1 0 1'))
