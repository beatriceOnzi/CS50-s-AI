import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11,
    }

    visitor_type = {
        "Returning_Visitor": 1,
        "New_Visitor": 0,
        "Other": 0
    }

    bool_map = {
        "TRUE": True,
        "FALSE": False
    }

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        label = []
        for row in reader:
            sample = []
            
            sample.append(int(row[0]))
            sample.append(float(row[1]))
            sample.append(int(row[2]))
            sample.append(float(row[3]))
            sample.append(int(row[4]))
            sample.extend(float(cell) for cell in row[5:10])
            sample.append(months[row[10]])
            sample.extend([float(cell) for cell in row[11:15]])
            sample.append(visitor_type[row[15]])
            sample.append(bool_map[row[16]])

            evidence.append(sample)
            label.append(bool_map[row[17]])

    return (evidence, label)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.

    KNeighborsClassifier(n_neighbors=1)
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)

    return neigh


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positive = 0
    true_negative = 0

    amount_true = 0
    amount_false = 0

    index = 0
    for l in labels:
        if l == 1:
            if l == predictions[index]:
                true_positive += 1
            amount_true += 1

        elif l == 0:
            if l == predictions[index]:
                true_negative += 1
            amount_false += 1

        index += 1

    sensitivity = true_positive / amount_true
    specificity = true_negative / amount_false

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
