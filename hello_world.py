''' Note that not all Python packages are guaranteed to have a __version__ attribute, so for some others it may fail, but for nltk and scikit-learn at least it will work. '''

import nltk
import dpath.util
#import sklearn

print('The nltk version is {}.'.format(nltk.__version__))
print('The dpath version is {}.'.format(dpath.__version__))
#print('The scikit-learn version is {}.'.format(sklearn.__version__))
print("fuck hello world")