from const import _EVALUTATION_THRESHOLDS_
from copy import deepcopy
class Evaluator:

    thresholds = deepcopy(_EVALUTATION_THRESHOLDS_)

    def set_threshold(self, key, value):
        self.thresholds[key] = value 

    def set_default_threshold(self):
        self.thresholds = deepcopy(_EVALUTATION_THRESHOLDS_)

    def get_threshold(self, key):
        return self.thresholds.get(key)

    

