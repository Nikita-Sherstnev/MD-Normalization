import sys

from fasttext import new_model, update_model, define_class

if __name__ == '__main__':
    if sys.argv[1] == 'new_model':
        if len(sys.argv) == 6:
            new_model(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    elif sys.argv[1] == 'update_model':
        if len(sys.argv) == 6:
            update_model(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    elif sys.argv[1] == 'define_class':
        define_class(sys.argv[2], sys.argv[3], sys.argv[4])
        



    

    
