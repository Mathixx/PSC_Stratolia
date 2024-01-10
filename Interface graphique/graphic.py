import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import SpanSelector

class StratosphericBalloonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stratospheric Balloon Simulation")

        self.create_widgets()

    def create_widgets(self):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('Latitude')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.label_status = ttk.Label(self, text="Balloon status: Waiting for update...")
        self.label_status.pack(side=tk.TOP)

        self.button_update = ttk.Button(self, text="Update", command=self.update_balloon)
        self.button_update.pack(side=tk.RIGHT)

        self.button_clear = ttk.Button(self, text="Clear", command=self.clear_plot)
        self.button_clear.pack(side=tk.RIGHT)

        self.button_quit = ttk.Button(self, text="Quit", command=self.destroy)
        self.button_quit.pack(side=tk.RIGHT)

        self.button_depart = ttk.Button(self, text="Départ", command=self.depart)
        self.button_depart.pack(side=tk.RIGHT)

        def onselect(xmin, xmax):
            if xmin > xmax:
                xmin, xmax = xmax, xmin
            diff = xmax - xmin
            self.ax.set_xlim(xmin - diff * 0.05, xmax + diff * 0.05)
            self.canvas.draw()

        self.selector = SpanSelector(self.ax, onselect, direction='horizontal', minspan=10, useblit=True,rectprops=dict(alpha=0.5, facecolor='red'))


    def update_balloon(self):
        # Here, you would implement the code to retrieve the new coordinates of the balloon
        # and add it to the plot.
        # For now, we generate random coordinates as an example.
        lat, lon = 50.74, 6.09 # random starting point in Germany
        altitude = 0 # random starting altitude

        self.ax.clear()
        self.ax.plot(lon, lat, marker='o', markersize=5, color='red', label='Balloon')
        self.ax.legend()
        self.canvas.draw()

        self.label_status['text'] = f"Balloon status: Latitude: {lat}, Longitude: {lon}, Altitude: {altitude} m"

    def clear_plot(self):
        self.ax.clear()
        self.canvas.draw()

    def depart(self):

        def on_ok():
            lat, lon = entry_lat.get(), entry_lon.get()
            entry_lat.delete(0, tk.END)
            entry_lon.delete(0, tk.END)
            self.ax.plot(lon, lat, marker='o', markersize=5, color='red', label='Balloon')
            self.ax.legend()
            self.canvas.draw()
            top.destroy()

        top = tk.Toplevel(self)
        top.title("Enter Latitude and Longitude")
        tk.Label(top, text="Latitude:").pack()
        entry_lat = tk.Entry(top)
        entry_lat.pack()
        tk.Label(top, text="Longitude:").pack()
        entry_lon = tk.Entry(top)  
        entry_lon.pack()
        tk.Button(top, text="OK", command=on_ok).pack()

if __name__ == "__main__":
    app = StratosphericBalloonApp()
    app.mainloop()