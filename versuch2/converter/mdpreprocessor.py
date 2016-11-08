#-----------------------------------------------------------------------------
# Copyright (c) 2016, Noah Huesser
#-----------------------------------------------------------------------------

from nbconvert.preprocessors import *
import re

class MarkdownPreprocessor(Preprocessor):
    
    def align_string(self, source):
        pre = '\\begin{gather*}'
        post = '\\end{gather*}'
        preresult = pre + source + post
        result = ''
        for l in preresult.split('\\$'):
            result += re.sub(
                r'\$(.*?)\$',
                lambda m: m.group(1),
                l,
                flags=re.MULTILINE|re.DOTALL
            )
        result = re.sub(
            r'(  )$',
            lambda m: '\\\\',
            result,
            flags=re.MULTILINE|re.DOTALL
        )
        result = re.sub(
            r'\<t\>(.*?)\<\/t\>',
            lambda m: ('\\text{' + m.group(1) + '}'),
            result,
            flags=re.MULTILINE|re.DOTALL
        )
        result = re.sub(
            r'(%)',
            lambda m: ('\\%'),
            result,
            flags=re.MULTILINE|re.DOTALL
        )
        return result

    def replace_center_tags(self,source):
        """
        Replace <center></center> with \begin{align*}\end{align*}
        """
        try:
            replaced = re.sub(
                r'<center>(.*?)</center>',
                lambda m: self.align_string(m.group(1)),
                source,
                flags=re.MULTILINE|re.DOTALL
            )
        except TypeError:
            replaced = source
        return replaced
    
    def replace_variables(self,source,variables):
        """
        Replace {{variablename}} with stored value
        """
        try:
            replaced = re.sub(r'{{(.*?)}}', lambda m: variables[m.group(1)] , source)
        except TypeError:
            replaced = source
        return replaced
    
    def replace_np_tags(self,source):
        """
        Replace <np/> with \newpage
        """
        try:
            replaced = re.sub(
                r'\<np\s/\>',
                lambda m: '\\newpage',
                source,
                flags=re.MULTILINE|re.DOTALL
            )
        except TypeError:
            replaced = source
        return replaced

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == "markdown":
            if hasattr(cell['metadata'], 'variables'):
                variables = cell['metadata']['variables']
                if len(variables) > 0:
                    cell.source = self.replace_variables(cell.source, variables)
            cell.source = self.replace_center_tags(cell.source)
            cell.source = self.replace_np_tags(cell.source)
        return cell, resources
