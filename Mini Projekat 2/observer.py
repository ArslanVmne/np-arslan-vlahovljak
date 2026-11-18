# Observer: trening obavještava posmatrače, a oni sami odlučuju šta će s porukom.
from abc import ABC, abstractmethod


class Observer(ABC):
    """Zajednički interfejs: svaki posmatrač mora imati update()."""

    @abstractmethod
    def update(self, message):
        pass


class ConsoleObserver(Observer):
    def update(self, message):
        print(f"  [Observer console] {message}")


class ListObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(message)


class Trainer:
    """Subjekat: čuva listu posmatrača i obavještava ih."""

    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

    def train(self, model, X, y):
        name = type(model).__name__
        self.notify(f"training started ({name})")
        model.fit(X, y)
        self.notify(f"training finished ({name})")
        return model
