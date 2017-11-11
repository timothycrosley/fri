import numpy as np
from sklearn.utils import check_random_state
from sklearn.datasets import make_regression

def _combFeat(n,strRelFeat,randomstate):
        # Split each strongly relevant feature into linear combination of it
        weakFeats = np.zeros((n,2))
        for x in range(2):
            cofact = 2 * randomstate.rand() - 1
            weakFeats[:,x] = cofact  * strRelFeat
        return weakFeats
def _dummyFeat(n,randomstate,scale=2):
        return  randomstate.rand(n)*scale - scale/2

def _repeatFeat(feats, i,randomstate):
        i_pick = randomstate.choice(i)
        return feats[:, i_pick]

def genData(**args):
    """ 
    Deprecated Method call generating Classification data
    """
    return genClassificationData(**args)

def _checkParam(n_samples: int=100, n_features: int=2,
                          n_redundant: int=0, strRel: int=1,
                          n_repeated: int=0, class_sep: float=0.2,
                          flip_y: float=0,noise: float = 1, **kwargs):
    if not 0 < n_samples:
        raise ValueError("We need at least one sample.")
    if not 0 < n_features:
        raise ValueError("We need at least one feature.")
    if not 0 <= flip_y < 1:
        raise ValueError("Flip percentage has to be between 0 and 1.")
    if not n_redundant%2 == 0:
        raise ValueError("Number of redundant features has to be even.")
    if not n_redundant+n_repeated+strRel<= n_features:
        raise ValueError("Inconsistent number of features")
    if strRel + n_redundant < 1:
        raise ValueError("No informative features.")
    print("Generating dataset with d={},n={},strongly={},weakly={}".format(n_features,n_samples,strRel,n_redundant))

def _fillVariableSpace(X_informative, random_state: object, n_samples: int=100, n_features: int=2,
                          n_redundant: int=0, strRel: int=1,
                          n_repeated: int=0,
                          noise: float = 1,**kwargs):
        X = np.zeros((int(n_samples), int(n_features)))
        X[:, :strRel] = X_informative[:, :strRel]
        holdout = X_informative[:, strRel:]
        i = strRel

        for x in range(len(holdout.T)):
            X[:, i:i + 2] = _combFeat(n_samples, holdout[:, x], random_state)
            i += 2

        for x in range(n_repeated):
            X[:, i] = _repeatFeat(X[:, :i], i, random_state)
            i += 1    
        for x in range(n_features - i):
            X[:, i] = _dummyFeat(n_samples, random_state, noise)
            i += 1

        return X

def genClassificationData(n_samples: int=100, n_features: int=2,
                          n_redundant: int=0, strRel: int=1,
                          n_repeated: int=0, class_sep: float=0.2,
                          flip_y: float=0, random_state: object=None):
    """Generate synthetic classification data
    
    Parameters
    ----------
    n_samples : int, optional
        Number of samples
    n_features : int, optional
        Number of features
    n_redundant : int, optional
        Number of features which are part of redundant subsets (weakly relevant)
    strRel : int, optional
        Number of features which are mandatory for the underlying model (strongly relevant)
    n_repeated : int, optional
        Number of features which are clones of existing ones. 
    class_sep : float, optional
        Size of region between classes.
    flip_y : float, optional
        Ratio of samples randomly switched to wrong class.
    random_state : object, optional
        Randomstate object used for generation.
    
    Returns
    -------
    X : array of shape [n_samples, n_features]
        The generated samples.
    y : array of shape [n_samples]
        The output classes.
    
    Raises
    ------
    ValueError
        Description
    ValueError
    Wrong parameters for specified amonut of features/samples.
    

    Examples
    ---------
    >>> X,y = genClassificationData(n_samples=200)
    Generating dataset with d=2,n=200,strongly=1,weakly=0
    >>> X.shape
    (200, 2)
    >>> y.shape
    (200,)
    """
    _checkParam(**locals())
    random_state = check_random_state(random_state)

    def genStrongRelFeatures(n, strRel,random_state, width=10, epsilon=0.05,):
        Y = np.ones(n)
        # Generate hyperplane consiting of strongly relevant features
        base = 0 # origin for now # TODO
        n_vec = random_state.uniform(0.2, 1, int(strRel)) * random_state.choice([1, -1], int(strRel))
        candidates = random_state.uniform(-width, width, (n, int(strRel)))
        distPlane = (np.inner(n_vec, candidates) - base)
        # reroll points which are too cloos to hyperplane
        close_candiate_mask = np.abs(distPlane) < epsilon
        while np.sum(close_candiate_mask) > 0:
            candidates[close_candiate_mask] = \
                random_state.uniform(-width, width, (np.sum(close_candiate_mask), int(strRel)))
            distPlane = (np.inner(n_vec, candidates) - base)
            close_candiate_mask = np.abs(distPlane) < epsilon

        Y[distPlane > epsilon] = 1
        Y[distPlane < -epsilon] = -1

        return candidates, Y

    X = np.zeros((n_samples,n_features))
    X_informative, Y = genStrongRelFeatures(n_samples,strRel+n_redundant/2,random_state,epsilon=class_sep)
    X = _fillVariableSpace(**locals())
 
    return X, Y


def genRegressionData(n_samples: int = 100, n_features: int = 2, n_redundant: int = 0, strRel: int = 1,
                      n_repeated: int = 0, noise: float = 1, random_state: object = None) -> object:
    """Generate synthetic regression data
    
    Parameters
    ----------
    n_samples : int, optional
        Number of samples
    n_features : int, optional
        Number of features
    n_redundant : int, optional
        Number of features which are part of redundant subsets (weakly relevant)
    strRel : int, optional
        Number of features which are mandatory for the underlying model (strongly relevant)
    n_repeated : int, optional
        Number of features which are clones of existing ones. 
    noise : float, optional
        Noise of the created samples around ground truth.
    random_state : object, optional
        Randomstate object used for generation.
    
    Returns
    -------
    X : array of shape [n_samples, n_features]
        The generated samples.
    y : array of shape [n_samples]
        The output values (target).
    
    Raises
    ------
    ValueError
    Wrong parameters for specified amonut of features/samples.
    """ 

    _checkParam(**locals())
    random_state = check_random_state(random_state)

    X = np.zeros((int(n_samples), int(n_features)))


    X_informative, Y = make_regression(n_features=int(strRel + n_redundant / 2),
                                        n_samples=int(n_samples),
                                        noise=noise,
                                        n_informative=int(strRel),
                                        random_state=random_state,
                                        shuffle=False)

    X = _fillVariableSpace(**locals())

    return X, Y
