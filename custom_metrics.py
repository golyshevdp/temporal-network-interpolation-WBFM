#Кастомные метрики для анализа экспериментов
import numpy as np


def interpolation_quality(truth_modularity, interp_modularity):
    """Вычислим среднеквадратическое отклонение интерполированной модулярности от истиной"""
    truth_modularity = np.array(truth_modularity)
    interp_modularity = np.array(interp_modularity)
    return np.sqrt(np.sum((truth_modularity - interp_modularity)**2))