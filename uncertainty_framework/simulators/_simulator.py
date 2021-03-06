import abc
from typing import Type, Union
import numpy as np

from uncertainty_framework.report._report import Report as ReportBaseClass
from uncertainty_framework.report.margins import MarginReport
from uncertainty_framework.report.console import ConsoleReport
from uncertainty_framework.report.plot import PlotReport


class Simulator(abc.ABC):
    def __init__(self):
        self.result = None

    """Simulator base class"""
    @abc.abstractmethod
    def run(self, **kwargs) -> np.ndarray:
        """
        The run function has to run the actual simulation 
        and needs at least to be implemented.
        It has to return a numpy array with all simulation 
        results in it, which can be used by reporting 
        and statistics tools.
        """
        pass

    def __call__(self, **kwargs) -> np.ndarray:
        self.result = self.run(**kwargs)
        return self.result

    def render(self, Report: Union[Type[ReportBaseClass], str] ='console', result: np.ndarray =None, **kwargs):
        """
        Render the results with the given class
        """
        # TODO: here we could accept some strings like 'html'
        # and so on to load default reporting classes
        
        # check if a result is calculated
        if result is None:
            result = self.result
        if result is None:
            raise RuntimeError("No simulation result found. Call this instance or pass the result matrix.")
        
        # load a predefined Report class
        if isinstance(Report, str):
            if Report.lower() == 'margin':
                Report = MarginReport
            elif Report.lower() == 'console':
                Report = ConsoleReport
            elif Report.lower() == 'plot':
                Report = PlotReport
            else:
                raise ValueError("'%s' is not a known Report option." % Report)
        
        # instantiate a report
        report = Report(result=result)

        # return the report
        return report(**kwargs)
