from pathlib import Path
from typing import List

import xlsxwriter

from orbis2.model.annotation import Annotation
from orbis2.model.run import Run


class ExcelFormat:
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    def export(self, run: Run, path: Path):

        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet('Text annotations')

        # formatting
        table_heading_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
        annotation_format = workbook.add_format({'italic': True, 'font_color': 'red'})

        # add table heading
        worksheet.merge_range('A1:C1', 'Document', table_heading_format)
        worksheet.merge_range('D1:G1', 'Annotations', table_heading_format)
        for col_num, cell_content in enumerate(('ID', 'Content', 'URL',
                                                'Start indices', 'End indices', 'Surface forms', 'Types')):
            worksheet.write(1, col_num, cell_content, table_heading_format)

        worksheet.set_default_row(20)
        worksheet.set_column(2, 1, 80)
        for row_num, (document, annotations) in enumerate(run.document_annotations.items(), start=2):
            # write document
            worksheet.write(row_num, 0, hash(document))
            worksheet.write(row_num, 1, document.content)
            worksheet.write(row_num, 2, document.key)

            # write annotations
            worksheet.write(row_num, 3, self.get_annotation_property(annotations, 'start_indices'))
            worksheet.write(row_num, 4, self.get_annotation_property(annotations, 'end_indices'))
            worksheet.write(row_num, 5, self.get_annotation_property(annotations, 'surface_forms'))
            worksheet.write(row_num, 6, self.get_annotation_property(annotations, 'annotation_type'))

        workbook.close()

    @staticmethod
    def get_annotation_property(annotations: List[Annotation], annotation_property: str) -> str:
        """
        Return:
             A list of values for the given annotation property.

        Note:
            Values belonging to multi-surface-form annotations are comma separated
        """
        property_extractor = ExcelFormat.get_property_extractor(annotation_property)
        return '; '.join([property_extractor(annotation) for annotation in annotations])

    @staticmethod
    def get_property_extractor(annotation_property: str):
        """
        Return:
            The helper method suitable for extracting the given property
        """
        if annotation_property in ('start_indices', 'end_indices', 'surface_forms'):
            return lambda annotation: ', '.join([str(idx) for idx in getattr(annotation, annotation_property)])
        elif annotation_property == 'annotation_type':
            return lambda annotation: annotation.annotation_type.name

        return lambda annotation: annotation
