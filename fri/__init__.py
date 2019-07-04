import logging

logging.basicConfig(level=logging.INFO)
import warnings
from enum import Enum

from fri.genData import genRegressionData, genClassificationData, genOrdinalRegressionData, quick_generate
from fri.main import FRIBase
from fri.model.classification import Classification
from fri.model.lupi_classification import LUPI_Classification
from fri.model.lupi_ordinal_regression import LUPI_OrdinalRegression
from fri.model.lupi_regression import LUPI_Regression
from fri.model.ordinal_regression import OrdinalRegression
from fri.model.ordinal_regression_imp import OrdinalRegression_Imp
from fri.model.regression import Regression
from fri.plot import plot_intervals


class ProblemName(Enum):
    CLASSIFICATION = Classification
    REGRESSION = Regression
    ORDINALREGRESSION = OrdinalRegression
    ORDINALREGRESSION_IMP = OrdinalRegression_Imp
    LUPI_CLASSIFICATION = LUPI_Classification
    LUPI_REGRESSION = LUPI_Regression
    LUPI_ORDREGRESSION = LUPI_OrdinalRegression


__all__ = ["genRegressionData", "genClassificationData", "genOrdinalRegressionData", "quick_generate",
           "FRIClassification", "FRIRegression", "FRIOrdinalRegression", "plot_intervals", ProblemName]

# Get version from versioneer
from fri._version import get_versions
__version__ = get_versions()['version']
del get_versions


def FRI(problem: ProblemName, random_state=None, n_jobs=1, verbose=0, n_param_search=50,
        n_probe_features=80, slack_regularization=0.1, slack_loss=0.1, **kwargs):
    """

    Parameters
    ----------
    problem : ProblemName or str
    Type of problem at hand.
    E.g. "classification", "regression", "ordinalregression"
    """

    if isinstance(problem, ProblemName):
        problemtype = problem.value
    else:
        if problem == "classification" or problem == "class":
            problemtype = Classification
        elif problem == "regression" or problem == "reg":
            problemtype = Regression
        elif problem == "ordinalregression" or problem == "ordreg":
            problemtype = OrdinalRegression
        elif problem == "lupi_classification" or problem == "lupi_class":
            problemtype = LUPI_Classification
        else:
            names = [enum.name.lower() for enum in ProblemName]

            print(f"Parameter 'problem' was not recognized or unset. Try one of {names}.")
            return None
    return FRIBase(problemtype, random_state=random_state, n_jobs=n_jobs, verbose=verbose,
                   n_param_search=n_param_search,
                   n_probe_features=n_probe_features,
                   w_l1_slack=slack_regularization,
                   loss_slack=slack_loss,
                   **kwargs)



def FRIClassification(**kwargs):
    warnings.warn(
        "This class call format is deprecated.",
        DeprecationWarning
    )

    typeprob = Classification
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return call_main_catch_old(typeprob,
                               **kwargs)


def FRIRegression(**kwargs):
    warnings.warn(
        "This class call format is deprecated.",
        DeprecationWarning
    )

    typeprob = Regression
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return call_main_catch_old(typeprob,
                               **kwargs)


def FRIOrdinalRegression(**kwargs):
    warnings.warn(
        "This class call format is deprecated.",
        DeprecationWarning
    )
    typeprob = OrdinalRegression
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return call_main_catch_old(typeprob,
                               **kwargs)


def call_main_catch_old(typeprob, optimum_deviation=0.1, n_resampling=80, iter_psearch=50, **kwargs):
    return FRIBase(typeprob, w1_l1_slack=optimum_deviation,
                   n_probe_features=n_resampling,
                   n_param_search=iter_psearch,
                   **kwargs)
