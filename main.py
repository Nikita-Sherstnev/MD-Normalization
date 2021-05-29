import sys

from fasttext import new_model, update_model, define_class
from metrics import count_metrics
from norm import Normalizer


if __name__ == '__main__':
    if sys.argv[1] == 'new_model':
        if len(sys.argv) == 6:
            new_model(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Error")

    elif sys.argv[1] == 'update_model':
        if len(sys.argv) == 6:
            update_model(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Error")

    elif sys.argv[1] == 'define_class':
        if len(sys.argv) == 5:
            define_class(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Error")

    elif sys.argv[1] == 'metrics':
        if len(sys.argv) == 5:
            count_metrics(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Error")

    elif sys.argv[1] == 'norm':
        if len(sys.argv) == 5:
            norm = Normalizer(sys.argv[2], sys.argv[3])
            norm.normalize_name(sys.argv[4])
        else:
            print("Error")
