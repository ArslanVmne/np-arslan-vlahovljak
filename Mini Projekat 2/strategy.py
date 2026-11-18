# Strategy: više metrika sa istim interfejsom, a biramo ih pri pozivu.
from abc import ABC, abstractmethod

from sklearn.metrics import accuracy_score, f1_score


class Metric(ABC):
    """Zajednički interfejs: svaka metrika mora imati compute()."""

    @abstractmethod
    def compute(self, y_true, y_pred):
        pass


class Accuracy(Metric):
    def compute(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)


class F1(Metric):
    def compute(self, y_true, y_pred):
        return f1_score(y_true, y_pred, average="macro")


def evaluate(metric, y_true, y_pred):
    """Ne zna koja je metrika u pitanju, samo poziva compute()."""
    return metric.compute(y_true, y_pred)
