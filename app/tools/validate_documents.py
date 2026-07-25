from typing import List

from app.schema.DocumentModel import DocumentModel,type_format
from app.schema.OCRstate import OCRresult
from app.schema.validation import ValidationResult

def validate_pages(document: DocumentModel) -> bool:
    return len(document.pages) > 0

def validate_page_elements(document: DocumentModel) -> bool:

    for page in document.pages:
        if len(page.elements) == 0:
            return False

    return True

def validate_reading_order(document: DocumentModel) -> bool:

    for page in document.pages:

        orders = [e.reading_order for e in page.elements]

        if orders != sorted(orders):
            return False

    return True


def validate_unique_ids(document: DocumentModel) -> bool:

    ids = []

    for page in document.pages:
        for element in page.elements:
            ids.append(element.id)

    return len(ids) == len(set(ids))


def validate_bbox(document: DocumentModel) -> bool:

    for page in document.pages:

        for element in page.elements:

            if len(element.bbox) != 4:
                return False

    return True


def validate_confidence(
    ocr: OCRresult,
    threshold: float = 0.65
) -> bool:

    return ocr.average_confidence >= threshold

def validate_word_count(
    document: DocumentModel,
    ocr: OCRresult,
    threshold: float = 0.80
) -> bool:

    ocr_words = len(ocr.plain_text.split())

    parsed_words = 0

    for page in document.pages:
        for element in page.elements:

            parsed_words += len(element.text.split())

    if ocr_words == 0:
        return False

    ratio = parsed_words / ocr_words

    return ratio >= threshold

def validate_unknown_blocks(
    document: DocumentModel,
    threshold: float = 0.30
) -> bool:

    total = 0
    unknown = 0

    for page in document.pages:
        for element in page.elements:

            total += 1

            if element.type == type_format.UNKNOWN:
                unknown += 1

    if total == 0:
        return False

    return (unknown / total) <= threshold


def validate_empty_text(document: DocumentModel) -> bool:

    for page in document.pages:
        for element in page.elements:

            if element.type != type_format.IMAGE:

                if element.text.strip() == "":
                    return False

    return True

def validate_page_numbers(document: DocumentModel) -> bool:

    expected = 1

    for page in document.pages:

        if page.page_no != expected:
            return False

        expected += 1

    return True

def validate_document(document, ocr):

    errors = []

    if not validate_pages(document):
        errors.append("Document contains no pages.")

    if not validate_word_count(document, ocr):
        errors.append("Significant word loss detected.")

    if not validate_confidence(ocr):
        errors.append("OCR confidence below threshold.")

    if not validate_bbox(document):
        errors.append("One or more bounding boxes are invalid.")

    return ValidationResult(
        passed=len(errors) == 0,
        errors=errors,
    )