# pipeline/evaluation/field_accuracy.py

def field_accuracy(gt: str, pred: str) -> int:
    """
    Strict field accuracy
    """
    if gt is None or pred is None:
        return 0

    return 1 if gt.strip() == pred.strip() else 0
