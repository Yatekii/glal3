from IPython.display import (
    display, display_html, display_png, display_svg
)
from IPython.core.pylabtools import print_figure
from IPython.display import Image, SVG, Math
import time
import inspect

class PrettyFigure:
    def __init__(self, figure, label=None, caption='Description missing'):
        self.figure = figure
        self.caption = caption
        self.label = label
        self.location_svg = None
        self.location_pdf = None
        self.location_png = None

    def _figure_data(self, format):
        data = print_figure(self.figure, format)
        return data

    def _svg_(self):
        svg_data = self._figure_data('svg')
        figure_location = 'images/figures/{0}.svg'.format(self.label.split(':')[1])
        if figure_location != self.location_svg:
            if self.location_svg != None:
                os.remove(self.location_svg)
            self.location_svg = figure_location
            svg = open(figure_location, 'w')
            svg.write(svg_data)
            svg.close()
        return svg_data

    def _png_(self):
        png_data = self._figure_data('png')
        figure_location = 'images/figures/{0}.png'.format(self.label.split(':')[1])
        if figure_location != self.location_png:
            if self.location_png != None:
                os.remove(self.location_png)
            self.location_png = figure_location
            png = open(figure_location, 'wb')
            png.write(png_data)
            png.close()
        return png_data

    def _pdf_(self):
        pdf_data = self._figure_data('pdf')
        figure_location = 'images/figures/{0}.pdf'.format(self.label.split(':')[1])
        if figure_location != self.location_pdf:
            if self.location_pdf != None:
                os.remove(self.location_pdf)
            self.location_pdf = figure_location
            pdf = open(figure_location, 'wb')
            pdf.write(pdf_data)
            pdf.close()
        return pdf_data

    def _repr_html_(self):
        self._png_()
        html_data ='''<img src="{0}" alt="{1}" style="display: block;margin-left: auto;margin-right: auto">
<p style="text-align:center">{1}</p>
'''
        return html_data.format(self.location_png, self.caption)

    def _repr_latex_(self):
        self._pdf_()
        latex_data = r'''\begin{figure*}[!htbp]
    \begin{center}\adjustimage{max size={0.9\linewidth}{0.4\paperheight}}{%s}\end{center}
    \caption{%s}
    \label{%s}
\end{figure*}
        ''' % (self.location_pdf, self.caption, self.label)
        return latex_data

    def show(self):
        display(self)
