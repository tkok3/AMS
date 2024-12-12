import flet as ft
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64  # Import base64 for encoding the image

def main(page: ft.Page):
    page.title = "Selectivity Graph App"
    
    n = 100
    pMin = -1
    
    # Initial values
    pMax = 3
    perm = 300
    x1 = 0.01

    def selectivity(pMax, perm, x1):
        x = [x1, 1 - x1]
        p = np.logspace(pMin, pMax, n)
        a = np.array([x + 1 / p + 1 / (perm - 1) for x in x])
        b = np.array([(4 * perm * x) / ((perm - 1) * p) for x in x])
        return p, 0.5 * p * (a - np.sqrt(a**2 - b))
    
    # Function to create the graph
    def create_graph(pMax, perm, x1):
        p, sl = selectivity(pMax, perm, x1)
        fig, (ax1, ax2) = plt.subplots(1, 2, layout = 'tight', figsize = (10, 6))
        
        ax1.plot(p, sl[0], label = 'Compound 1')
        #ax1.plot(p, sl[1], label = 'Compound 2')
        ax1.set_title("Permeate concentration")
        ax1.set_xlabel("Pressure ratio [-]")
        ax1.set_ylabel("y [-]")
        ax1.grid(True)
        ax1.set_ylim([0, 1])  # Set ylim to [0, 1]
        
        ax2.plot(p, sl[0]/sl[1])
        ax2.set_title("Selectivity")
        ax2.set_xlabel("Pressure ratio [-]")
        ax2.set_ylabel("Selectivity [-]")
        ax2.set_yscale('log')
        ax2.set_xscale('log')
        ax2.set_ylim([0.001, 1])
        ax2.grid(True)
        
        # Save plot to buffer
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf
                
    # Update the graph dynamically
    def update_graph(e=None):
        buf = create_graph(float(pMax_field.value), float(perm_field.value), float(x_field.value))
        graph_image.src_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        graph_image.update()

    # Text fields to display and edit pMax, perm, and x
    pMax_field = ft.TextField(label="pMax", value=str(pMax), width=150, on_change=update_graph)
    perm_field = ft.TextField(label="perm", value=str(perm), width=150, on_change=update_graph)
    x_field = ft.TextField(label="x1", value=str(x1), width=150, on_change=update_graph)

    # Image to display the graph (initialize with default values)
    initial_graph = create_graph(pMax, perm, x1)
    graph_image = ft.Image(src_base64=base64.b64encode(initial_graph.getvalue()).decode("utf-8"))

    # Add controls to the page
    page.add(
        graph_image,
        ft.Row([pMax_field, perm_field, x_field]),
    )

# Run the app
ft.app(target=main)
