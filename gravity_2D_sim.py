import time

from graphing_interface import Animation2DWindow
import math
import numpy as np


def recalculate_objects(object1, object2, accuracy):
    force = ((6.67e-11 * object1[-1] * object2[-1]) / ((object2[0] - object1[0]) ** 2 + (object2[1] - object1[1]) ** 2)) * accuracy
    try:
        angle = math.atan((object2[0] - object1[0]) / (object2[1] - object1[1]))
    except ZeroDivisionError:
        if object1[0] - object2[0] > 0:
            angle = math.pi
        else:
            angle = -math.pi

    if angle >= 0 and object1[1] > object2[1]:
        object1[2] -= (force * math.sin(angle)) / object1[-1]
        object2[2] += (force * math.sin(angle)) / object2[-1]
        object1[3] -= (force * math.cos(angle)) / object1[-1]
        object2[3] += (force * math.cos(angle)) / object2[-1]
    elif angle >= 0 and object1[1] < object2[1]:
        object1[2] += (force * math.sin(angle)) / object1[-1]
        object2[2] -= (force * math.sin(angle)) / object2[-1]
        object1[3] += (force * math.cos(angle)) / object1[-1]
        object2[3] -= (force * math.cos(angle)) / object2[-1]
    elif object1[0] > object2[0]:
        object1[2] += (force * math.sin(angle)) / object1[-1]
        object2[2] -= (force * math.sin(angle)) / object2[-1]
        object1[3] += (force * math.cos(angle)) / object1[-1]
        object2[3] -= (force * math.cos(angle)) / object2[-1]
    else:
        object1[2] -= (force * math.sin(angle)) / object1[-1]
        object2[2] += (force * math.sin(angle)) / object2[-1]
        object1[3] -= (force * math.cos(angle)) / object1[-1]
        object2[3] += (force * math.cos(angle)) / object2[-1]


def process_velocity(object1, accuracy):
    object1[0] += object1[2] * accuracy
    object1[1] += object1[3] * accuracy


distance = 1.4786e11
window = Animation2DWindow(1.7, 5)
sun = [0, 0, 0, 0, 1.989e30]
mercury = [0, -4.6e10, -5.898e4, 0, 3.3010e23]
venus = [-0.71843*distance, 0, 0, 3.526e4, 4.8675e24]
earth = [0, 1.47098074e11, 3.029e4, 0, 5.972e24]
mars = [1.3814*distance, 0, 0, -2.65e4, 6.39e23]
objects = [sun, mercury, venus, earth, mars]
# objects = [sun, mars]
accuracy_per_render = 100000
time_period = 0.1
accuracy_multiplier = 100
start = time.perf_counter()
while True:
    total_accuracy = 0
    prev_frac = 0
    backwards = 0
    while True:
        highest_velocity = max(objects, key=lambda x: x[2]**2 + x[3]**2)
        highest_velocity = math.sqrt(highest_velocity[2] ** 2 + highest_velocity[3] ** 2)
        accuracy = distance/(highest_velocity ** 1.5 * accuracy_multiplier)
        accuracy = min(accuracy, 2000)
        for i in range(len(objects) - 1):
            for j in range(i+1, len(objects)):
                recalculate_objects(objects[i], objects[j], accuracy)
        for object1 in objects:
            process_velocity(object1, accuracy)
        total_accuracy += accuracy
        if total_accuracy >= (accuracy_per_render * (time.perf_counter() - start) / time_period):
            break
        frac = total_accuracy / (accuracy_per_render * (time.perf_counter() - start) / time_period)
        if frac < prev_frac:
            if backwards > 10000:
                print("simulation may be too fast")
                backwards = 0
            else:
                backwards += 1
        prev_frac = frac
    start = time.perf_counter()
    window.process_frame(((sun[0]/distance, sun[1]/distance),
                          (mercury[0]/distance, mercury[1]/distance),
                          (venus[0]/distance, venus[1]/distance),
                          (earth[0]/distance, earth[1]/distance),
                          (mars[0]/distance, mars[1]/distance)),
                         np.array([0.1, 0.05, 0.05, 0.05, 0.05]))
    # window.process_frame(((sun[0]/distance, sun[1]/distance),
    #                       (mars[0]/distance, mars[1]/distance)),
    #                      np.array([0.1, 0.05]))