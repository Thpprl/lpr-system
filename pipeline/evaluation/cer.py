# pipeline/evaluation/cer.py
import Levenshtein

def cer(gt: str, pred: str) -> float:
    """
    Character Error Rate
    """
    if not gt:
        return 1.0 if pred else 0.0

    distance = Levenshtein.distance(gt, pred)
    return distance / len(gt)
