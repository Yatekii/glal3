c = get_config()
c.Exporter.preprocessors = [ 'converter.bibpreprocessor.BibTexPreprocessor', 'converter.mdpreprocessor.MarkdownPreprocessor' ]
c.TemplateExporter.template_path = ['.']
c.Exporter.template_file = 'converter/template'
c.NbConvertApp.export_format = 'pdf'
