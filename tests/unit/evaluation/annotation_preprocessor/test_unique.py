from orbis2.evaluation.annotation_preprocessor.unique import UniqueSlotValue
from orbis2.model.annotation import get_mock_annotation as Annotation
from orbis2.model.metadata import Metadata


def test_unique_slot_value():
    """
    Test the normalization of Annotations to slot values.
    """
    annotations = [Annotation(key=12,
                              surface_forms='BSc',
                              start_indices=7,
                              end_indices=12,
                              metadata=[Metadata('parititon', 'requirement')]),
                   Annotation(key=72,
                              surface_forms='BSc',
                              start_indices=37,
                              end_indices=40,
                              metadata=[Metadata('parititon', 'requirement')]),
                   Annotation(key=12,
                              surface_forms='BSc',
                              start_indices=37,
                              end_indices=42,
                              metadata=[Metadata('parititon', 'requirement')]),
                   ]

    assert UniqueSlotValue().preprocess(annotations) == [
        Annotation(key=12,
                   surface_forms='BSc',
                   start_indices=0,
                   end_indices=5,
                   metadata=[Metadata('parititon', 'requirement')]
                   ),
        Annotation(key=72,
                   surface_forms='BSc',
                   start_indices=0,
                   end_indices=3,
                   metadata=[Metadata('parititon', 'requirement')]
                   )
    ]
