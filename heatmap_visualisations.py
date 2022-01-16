import matplotlib.pyplot as plt
import numpy as np

class heatmap_visualisations:
    def __init__(self, imageData):
        self.imageData = imageData

    def show_HeatmapVid(self):
        plt.ion()
        
        fig, ax = plt.subplots()
        im = ax.imshow(self.imageData, interpolation='bicubic', cmap='hot') ##interpolation='bicubic', 

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("", rotation=-90, va="bottom")

        return fig, im


    def show_HeatmapImg(self):     
        fig, ax = plt.subplots()

        plt.axis('off')

        im = ax.imshow(self.imageData, cmap='hot') ##interpolation='bicubic', 

        ## For comparison ##   
        # methods = ['bicubic', None]
        # for ax, interp_method in zip(ax.flat, methods):
        #     im = ax.imshow(self.imageData, interpolation=interp_method, cmap='jet')

        # # Create colorbar
        # cbar = ax.figure.colorbar(im, ax=ax)
        # cbar.ax.set_ylabel("", rotation=-90, va="bottom")

        plt.tight_layout()
        plt.savefig("test_data/newfigure.jpg", bbox_inches='tight',pad_inches = 0)
        plt.show()


    def show_HMIntOpt(self):
        methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

        fig, ax = plt.subplots(nrows=3, ncols=6, figsize=(18,12))
        for ax, interp_method in zip(ax.flat, methods):
            ax.imshow(self.imageData, interpolation=interp_method, cmap='jet')
            ax.set_title(str(interp_method))

        plt.tight_layout()
        plt.show()