import numpy
from matplotlib import pyplot as plt
from scipy import interpolate


class VoltageData:
    """Class for handling a set of measurements of the voltage at different
    times."""   #useful to write, 'cause if I use 'help()' it return this text

    #first we define the constructor
    def __init__(self, times, voltages):
        """ times and voltages are two iterables of the same length."""
        t = numpy.array(times, dtype=numpy.float64)
        v = numpy.array(voltages, dtype=numpy.float64)
        #built a 2d matrix with data
        self._data = numpy.column_stack([t, v]) #private attribute
        self.spline = interpolate.InterpolatedUnivariateSpline(self.timestamps,
                                                               self.voltages,
                                                               k=3) #spline cubic
#define attribute times and voltages
    @property  #decoratore
    def timestamps(self):
        return self._data[:, 0] #all rows, first column

    @property
    def voltages(self):
        return self._data[:, 1] #all rows, second column

#define the method len
    def __len__(self):
        """ Return the number of entries (measurements)."""
        return len(self._data)

#define method to make possible the access at the object of the class by []
    def __getitem__(self, index):
        """Random access"""  
        return self._data[index]

#implement the iter method (now it is possible to iterate)
    def __iter__(self):
        return iter(self._data)  #use built-in iter of python

#define method to print values 
    def __str__(self):
        """ Print values row-by-row."""
        row_fmt = '{:d}) {:.1f} {:.2f}' #indice/t/v
        output_rows = []
        for i, entry in enumerate(self):  #iterare tenendo traccia dell'indice
            row = row_fmt.format(i, entry[0], entry[1])
            output_rows.append(row)
        return '\n'.join(output_rows)   #concatena elementi lista
                                        #mettendo in mezzo \n
        
        #return '\n'.join([row_fmt.format(i, entry[0], entry[1]) \
        #                  for i, entry in enumerate(self)])

#method to plot the data
    def plot(self, ax=None, fmt='bo--', **kwargs):
        """ Plot the data using matplotlib.pyplot."""
        if ax is not None:   #if figure is not define, define it
            plt.sca(ax)
        else:                #otherwise use the one that exist 
            plt.figure('voltages vs times')
        plt.plot(self.timestamps, self.voltages, fmt, **kwargs)
        #**kwargs can contain an arbitrary number of argument
        plt.xlabel('Time [s]')
        plt.ylabel('Voltage [mV]')
        plt.grid(True)
        return plt.gca()

    def __call__(self, t):
        """ Return the voltage value interpolated at time t"""
        return self.spline(t)


if __name__ == '__main__':
    """ Here we test the functionalities of our class. These are not proper
    UnitTest - which you will se in a future lesson."""
    # Load some data
    t, v = numpy.loadtxt('sample_data_file.txt', unpack=True)
    # Thest the constructor
    v_data = VoltageData(t, v)
    # Test len()
    assert len(v_data) == len(t)
    # Test the timestamps attribute  #testing that all values of v_data==v
    assert numpy.all(v_data.voltages == v)
    # Test the voltages attribute
    assert numpy.all(v_data.timestamps == t)
    # Test access using square parenthesis
    assert v_data[3, 1] == v[3]
    assert v_data[-1, 0] == t[-1]
    # Test slicing
    assert numpy.all(v_data[1:5, 1] == v[1:5])
    # Test iteration
    for i, entry in enumerate(v_data):
        assert entry[0] == t[i]
        assert entry[1] == v[i]
    # Test printing
    print(v_data)   #print() call str if the object that I pass is not a string
    # Test plotting
    v_data.plot(fmt='ko', markersize=5, label='normal voltage')
    x_grid = numpy.linspace(min(t), max(t), 200)
    plt.plot(x_grid, v_data(x_grid), 'r-', label='spline')
    plt.legend()
    plt.show()
