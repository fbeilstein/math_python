import implementation_tasks
from levels.level_2_statistics import Level2Statistics

class Level3Smoothing(Level2Statistics):
    def make_prediction(self):
        return implementation_tasks.predict_with_fallback(self.history, self.order, self.counts_dict)
