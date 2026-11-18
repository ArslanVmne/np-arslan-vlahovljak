# Factory: jedna funkcija koja na osnovu imena vraća odgovarajući model.
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def create_model(name):
    """Vraća neistrenirani model za ime "linear", "tree" ili "knn"."""
    if name == "linear":
        return LogisticRegression(max_iter=200)
    if name == "tree":
        return DecisionTreeClassifier(random_state=0)
    if name == "knn":
        return KNeighborsClassifier(n_neighbors=3)
    raise ValueError(f"Unknown model name: {name}")
