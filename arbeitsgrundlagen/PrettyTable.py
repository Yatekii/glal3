# class PrettyTable

import math

class PrettyTable(list):
    """ Overridden list class which takes a 2-dimensional list of 
        the form [[1,2,3],[4,5,6]], and renders HTML and LaTeX Table in 
        IPython Notebook. For LaTeX export two styles can be chosen."""
    def __init__(self, initlist=[], extra_header=None, entries_per_column=None, significant_digits=4, print_latex_longtable=True):
        self.print_latex_longtable = print_latex_longtable
        self.entries_per_column = entries_per_column
        self.significant_digits = significant_digits
        if extra_header is not None:
            extra_header = [e.replace('%', '\\%') for e in extra_header]
            if len(initlist[0]) != len(extra_header):
                raise ValueError("Header list must have same length as data has columns.")
            initlist = [extra_header]+list(initlist)
        super(PrettyTable, self).__init__(initlist)
    
    def latex_table_tabular(self):
        latex = ["\\begin{tabular}"]
        latex.append("{"+"|".join((["l"]*len(self[0])))+"}\n")
        for row in self:
            latex.append(" & ".join(map(format, row)))
            latex.append("\\\\ \n")
        latex.append("\\end{tabular}")
        return ''.join(latex)
    
    def latex_longtable(self):
        latex = ["\\begin{longtable}[]{@{}"]
        l = len(self) - 1
        li = len(self[0])
        latex.append("l" * (li * math.ceil(l / self.entries_per_column)))
        latex.append("@{}}\n")
        latex.append("\\toprule\\addlinespace\n")
        line = (" & ".join(map(format, self[0])))
        latex.append((line  + " & ") * (math.ceil(l / self.entries_per_column) - 1))
        print(latex)
        latex.append(line)
        print(latex)
        latex.append("\\\\\\addlinespace \n")
        latex.append("\\midrule\\endhead\n")
        rows = []
        rows_done = 0
        for row in self[1:]:
            if rows_done < self.entries_per_column:
                rows.append(" & ".join(map(('{0:.' + str(self.significant_digits) + 'f}').format, row)))
                rows.append("\\\\\\addlinespace \n")
            else:
                rows[(rows_done % self.entries_per_column) * 2] += " & " + " & ".join(map(('{0:.' + str(self.significant_digits) + 'f}').format, row))
            rows_done += 1
        latex.extend(rows)
        latex.append("\\bottomrule \n \\end{longtable}")
        return ''.join(latex)
    
    def _repr_html_(self):
        html = ["<table>"]
        for row in self:
            html.append("<tr>")
            for col in row:
                html.append("<td>{0}</td>".format(col))
            html.append("</tr>")
        html.append("</table>")
        return ''.join(html)
    
    def _repr_latex_(self):
        if self.print_latex_longtable: 
            return self.latex_longtable()
        else: 
            return self.latex_table_tabular()