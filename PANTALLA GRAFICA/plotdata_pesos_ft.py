# importing required modules
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
import os

class plotdata_pesos_ft:

    def __init__(self, frame):
        # creating an empty plot/frame
        if os.environ.get('DISPLAY', '') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')

        self.fig = plt.figure()
        self.update = True
        self.ax = plt.axes(xlim=(0, 100), ylim=(-2, 2))
        self.ax.grid(True)
        #self.line, = self.ax.plot([], [], lw=2)
        self.ax.axhline(y=0, color="black", linestyle="--")
        self.lineb0, = self.ax.plot([], [], 'g-', label="b0", lw=1)
        self.linea0, = self.ax.plot([], [], 'b-', label="a0", lw=1)
        self.linea1, = self.ax.plot([], [], 'r-', label="a1", lw=1)
        self.xdata_b0 = []
        self.ydata_b0 = []
        self.xdata_a0 = []
        self.ydata_a0 = []
        self.xdata_a1 = []
        self.ydata_a1 = []
        canvas = FigureCanvasTkAgg(self.fig, master=frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.X, expand=0)

        # call the animator
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func=None,
                                       frames=500, interval=100, blit=False)


    def addPoint(self, point):
        self.xdata_b0.append(point[0][0])
        self.ydata_b0.append(point[0][1])
        self.xdata_a0.append(point[1][0])
        self.ydata_a0.append(point[1][1])
        self.xdata_a1.append(point[2][0])
        self.ydata_a1.append(point[2][1])

        self.update = True

    def getXDataSize(self):
        return len(plt.getp(self.lineb0, 'xdata'))

    def hide_show_line(self, states):
        if(self.xdata_b0):
            lines = [self.lineb0, self.linea0, self.linea1]
            for i in range(len(states)):
                lines[i].set_visible(states[i])

    def clear(self):
        self.xdata_b0 = []
        self.ydata_b0 = []
        self.xdata_a0 = []
        self.ydata_a0 = []
        self.xdata_a1 = []
        self.ydata_a1 = []
        self.ax.set_xlim(0, 100)

    # animation function
    def animate(self, i):
        if self.update:
            self.lineb0.set_data(self.xdata_b0, self.ydata_b0)
            self.linea0.set_data(self.xdata_a0, self.ydata_a0)
            self.linea1.set_data(self.xdata_a1, self.ydata_a1)
            if len(self.xdata_b0) > 1:
                i_min = 0
                i_max = len(self.xdata_b0)
                if self.xdata_b0[-1] > 100:
                    x_min = self.xdata_b0[-1] - 100
                    x_max = self.xdata_b0[-1]
                    i_min = i_max - 100
                    self.ax.set_xlim(x_min, x_max)
                y_max = max([max(self.ydata_b0[i_min:i_max]), max(self.ydata_a0[i_min:i_max]),
                                 max(self.ydata_a1[i_min:i_max]),2])
                y_min = min([min(self.ydata_b0[i_min:i_max]), min(self.ydata_a0[i_min:i_max]),
                                 min(self.ydata_a1[i_min:i_max]),-2])
                self.ax.set_ylim(y_min, y_max)

        # return line object
        return self.lineb0, self.linea0, self.linea1

