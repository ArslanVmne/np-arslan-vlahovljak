import pytest
from decorator_timing import timed
from factory import create_model
from observer import ConsoleObserver, ListObserver, Trainer
from template import Experiment, ScaledExperiment
from strategy import Accuracy, F1, Metric, evaluate
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


# ---------- Factory ----------
@pytest.mark.parametrize("name, expected", [
    ("linear", LogisticRegression),
    ("tree", DecisionTreeClassifier),
    ("knn", KNeighborsClassifier),
])
def test_factory_returns_correct_model(name, expected):
    assert isinstance(create_model(name), expected)


def test_factory_unknown_name_raises_error():
    with pytest.raises(ValueError):
        create_model("svm")


# ---------- Strategy ----------
def test_accuracy_perfect_prediction():
    assert evaluate(Accuracy(), [0, 1, 2], [0, 1, 2]) == 1.0


def test_accuracy_half_correct():
    assert evaluate(Accuracy(), [0, 1, 0, 1], [0, 1, 1, 0]) == 0.5


def test_f1_perfect_prediction():
    assert evaluate(F1(), [0, 1, 2], [0, 1, 2]) == 1.0


def test_metric_is_abstract():
    with pytest.raises(TypeError):
        Metric()


# ---------- Observer ----------
def test_list_observer_receives_start_and_finish():
    trainer, saved = Trainer(), ListObserver()
    trainer.add_observer(saved)
    trainer.train(create_model("tree"), [[0], [1]], [0, 1])
    assert saved.messages == ["training started (DecisionTreeClassifier)",
                              "training finished (DecisionTreeClassifier)"]


def test_all_observers_are_notified():
    trainer, first, second = Trainer(), ListObserver(), ListObserver()
    trainer.add_observer(first)
    trainer.add_observer(second)
    trainer.notify("hello")
    assert first.messages == second.messages == ["hello"]


def test_console_observer_prints_message(capsys):
    ConsoleObserver().update("hello")
    assert "hello" in capsys.readouterr().out


# ---------- Decorator ----------
@timed
def add(a, b):
    return a + b


def test_timed_returns_original_result():
    assert add(2, 3) == 5


def test_timed_prints_function_name_and_time(capsys):
    add(1, 1)
    out = capsys.readouterr().out
    assert "add" in out and "took" in out


def test_timed_keeps_function_name():
    assert add.__name__ == "add"


# ---------- Template Method ----------
def test_experiment_runs_and_returns_score():
    score = Experiment("tree", Accuracy()).run()
    assert 0.0 <= score <= 1.0


def test_experiment_steps_run_in_fixed_order():
    calls = []

    class Recording(Experiment):
        def load_data(self):
            calls.append("load")
            super().load_data()

        def train(self):
            calls.append("train")
            super().train()

        def evaluate(self):
            calls.append("evaluate")
            return super().evaluate()

        def report(self, score):
            calls.append("report")

    Recording("knn", Accuracy()).run()
    assert calls == ["load", "train", "evaluate", "report"]


def test_scaled_experiment_changes_only_data_step():
    experiment = ScaledExperiment("knn", F1())
    experiment.run()
    assert abs(experiment.X_train.mean()) < 1e-6  # skalirani podaci imaju prosjek ~0


def test_experiment_notifies_observers():
    saved = ListObserver()
    Experiment("linear", Accuracy(), observers=[saved]).run()
    assert len(saved.messages) == 2
