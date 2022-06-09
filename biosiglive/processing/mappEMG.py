"""
Add all mappEMG processing functions here
"""

import numpy as np
import pandas as pd
import os


class EMGprocess:

    def __init__(self):
        """
        Initialize the class.
        """
        self.amplitude_points = [(0, 0), (0.077, 3.683), (0.159, 11.049), (0.714, 107.315),(0.795, 117.094), (0.868, 121.793), (0.945, 125.222), (1, 127)]
        self.frequency_points = [(0, 10.414), (0.032, 18.54199999), (0.082, 27.178), (0.155, 35.814), (0.985, 105.664)]
        #self.prev_values = np.array() # array is past values of emg (we can keep only last 500 values to not use too much mem)
        self.x_emg = 0 # current raw value of emg 
        self.x_emg_smoothed = 0 # current inputted x smoothed
        self.x_emg_scaled = 0
        self.input_started = False
        

    # function to update currently passed emg value, as well as updating the previous values array
    def input(self, x): 
        '''
        function that takes emg input (in %MVC)
        updates x_emg attribute of object
        '''
        self.x_emg = float(x)
        if self.input_started == False: # if this is the first input passed, then the smoothed input is the same as the first input
            self.x_emg_smoothed = float(x) 
        self.input_started = True
        # np.append(self.prev_values, x)
        # if len(self.prev_values) > 500:
        #     self.prev_values = self.prev_values[len(self.prev_values)-100:len(self.prev_values)] # updating prev values to only be the last 100 values

    def clip(self):
        '''
        clips %MVC input such that it stays between 0 and 1
        '''
        if self.x_emg > 1:
            self.x_emg = 1
        if self.x_emg < 0:
            self.emg = 0
        
    # @staticmethod
    # def local_maxima(array):
    #     try:
    #         return np.amax(array[100:])
    #     except ValueError:  # should happen if inputed array is less than 100 values
    #         return np.amax(array)
    
    def slide(self, slide_up = 1/5, slide_down = 1/5):
        if self.x_emg > self.x_emg_smoothed: # if cur x value is bigger than prev computed smoothed val
            self.x_emg_smoothed = self.x_emg_smoothed + (self.x_emg - self.x_emg_smoothed) / slide_up
            
        elif self.x_emg < self.x_emg_smoothed: # if cur x value is smaller than prev computed val
            self.x_emg_smoothed = self.x_emg_smoothed + (self.x_emg - self.x_emg_smoothed) / slide_down

        # if cur raw value is the same as the same as prev computed, keep that value (hence not do anything)
        self.x_emg_scaled = self.x_emg_smoothed
        return self.x_emg_smoothed
   

    def scale(self,expected_max):
        self.x_emg_scaled = self.x_emg_scaled/expected_max
        return self.x_emg_scaled

        

class Mapper:

    def __init__(self,n): 
        """
        Initialize the class.
        """
        self.amplitude_points = [(0, 0), (0.077, 3.683), (0.159, 11.049), (0.714, 107.315),(0.795, 117.094), (0.868, 121.793), (0.945, 125.222), (1, 127)]
        self.frequency_points = [(0, 10.414), (0.032, 18.54199999), (0.082, 27.178), (0.155, 35.814), (0.985, 105.664)]
        self.n = n
        self.inputs = dict()
        for i in range(1,n+1):
            self.inputs[i] = 0.0
        self.weighted_emgs = 0.0
        self.freqthreshold = 0.0
        self.amplthreshold = 0.0
        self.yminf = 0.0
        self.ymina = 0.0
        self.ymaxf = 127.0
        self.ymaxa = 127.0
    
    
    def input(self, x, n):
        """
        Sets nth emg to value x
        """
        self.inputs[n] = x

    
    
    def weighted_average(self, weights):
        """
        Takes list of weights argument, index matches emg num
        Returns weighted average
        """
        if len(weights) != len(self.inputs):
            print('Number of inputed weights does not match number of emg used')
            return False

        sum = 0
        numerator = 0
        for i,w in enumerate(weights):
            sum += w
            numerator += w*self.inputs[i+1]
        self.weighted_emgs = numerator/sum
        return numerator/sum

    
    
    def changeMapping(self, new_points, mapping):
        '''
        Updates the sigmoidal mapping

        Arguments
        -----
        new_points: points to add to define the mapping, should be a list of tuples [(x1,y1),(x2,y2),..] 
        mapping: f or a, string f = change frequency mapping, string a = change amplitude mapping
        '''
        
        for p in set(new_points): # appending to corresponding list
            if mapping == 'f':
                self.frequency_points.append(p)
            elif mapping == 'a':
                self.amplitude_points.append(p)

        # sorting
        if mapping == 'f':
            self.frequency_points.sort(key=lambda tup: tup[0])  # sorting the list according to x values
        elif mapping == 'a':
            self.amplitude_points.sort(key=lambda tup: tup[0])  # sorting the list according to x values


    def addThreshold(self, threshold, mapping):
        '''
        updates threshold values used in mapper

        Arguments:
        ---
        threshold: threshold value
        mapping: 'f' or 'a', 'f' = frequency mapper & 'a' = amplitude mapper
        '''
        if mapping == 'f':
            self.freqthreshold = threshold
        if mapping == 'a':
            self.amplthreshold = threshold
    

    def changeMinY(self, y, mapping):
        '''
        updates minimal y value in the mapping

        Arguments:
        ---
        y: y value
        mapping: 'f' or 'a', 'f' = frequency mapper & 'a' = amplitude mapper
        '''
        if mapping == 'f':
            self.yminf = y
        if mapping == 'a':
            self.ymina = y

        
    def mapper(self, x, mapping, **extra):
        '''
        given a list of points in a function, outputs y value of x 

        Arguments
        ---
        x: value we want a mapping for (should be from 0 to 1)
        mapping: 'f' or 'a', 'f' = frequency mapper & 'a' = amplitude mapper
        '''

        if mapping == 'f':
            points = self.frequency_points
            threshold = self.freqthreshold
            ymin = self.yminf
        elif mapping == 'a':
            points = self.amplitude_points
            threshold = self.amplthreshold
            ymin = self.ymina
        
        if x < threshold:  # if x is less than threshold
            return ymin

        prev_point = points[0]  # getting first point
        for point in points[1:]:
            if x == prev_point[0]:
                return prev_point[1]  # return y value of that point
            if prev_point[0] < x < point[0]:
                # compute equation of line
                m = (point[1] - prev_point[1]) / (point[0] - prev_point[0])
                b = prev_point[1] - m * prev_point[0]
                return m * x + b  # return corresponding y using equation of line between two points
            if x == point[0]:
                return point[1]

    
    def toFreqAmpl(self,x):
        '''
        takes x and outputs its mapping as a tuple of the form (amplitude,frequency)
        '''
        f = self.mapper(x,'f')
        a = self.mapper(x,'a')
        return (a,f)
