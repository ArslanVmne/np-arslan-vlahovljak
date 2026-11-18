# Demo: svi šabloni zajedno na iris skupu.
from observer import ConsoleObserver, ListObserver
from strategy import Accuracy, F1
from template import Experiment, ScaledExperiment

saved = ListObserver()

print("=== 1) Factory + Strategy: tri modela, metrika Accuracy ===")
for name in ["linear", "tree", "knn"]:
    Experiment(name, Accuracy(), observers=[saved]).run()

print("\n=== 2) Strategy: isti model (knn), druga metrika (F1) ===")
Experiment("knn", F1()).run()

print("\n=== 3) Observer: ConsoleObserver ispisuje poruke treninga ===")
Experiment("tree", Accuracy(), observers=[ConsoleObserver()]).run()

print("\n=== 4) Template Method: ScaledExperiment mijenja samo load_data ===")
ScaledExperiment("knn", Accuracy()).run()

print("\n=== 5) Observer: ListObserver je cuvao poruke iz koraka 1 ===")
for message in saved.messages:
    print(" ", message)
