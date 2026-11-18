# Template Method: run() fiksira redoslijed koraka, podklase mijenjaju samo pojedinačni korak.
from decorator_timing import timed
from factory import create_model
from observer import Trainer
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from strategy import evaluate


class Experiment:
    def __init__(self, model_name, metric, observers=()):
        self.model_name = model_name
        self.metric = metric
        self.trainer = Trainer()
        for observer in observers:
            self.trainer.add_observer(observer)

    def run(self):
        """Template metoda: redoslijed se ne mijenja."""
        self.load_data()
        self.train()
        score = self.evaluate()
        self.report(score)
        return score

    def load_data(self):
        X, y = load_iris(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.3, random_state=0)

    @timed
    def train(self):
        self.model = create_model(self.model_name)  # Factory
        self.trainer.train(self.model, self.X_train, self.y_train)  # Observer

    def evaluate(self):
        predictions = self.model.predict(self.X_test)
        return evaluate(self.metric, self.y_test, predictions)  # Strategy

    def report(self, score):
        print(f"  Result: model={self.model_name}, metric={type(self.metric).__name__}, score={score:.3f}")


class ScaledExperiment(Experiment):
    """Mijenja samo load_data: podatke dodatno skalira."""

    def load_data(self):
        super().load_data()
        scaler = StandardScaler().fit(self.X_train)
        self.X_train = scaler.transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)
