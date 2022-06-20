#Алгоритм интерполяции графов на основе WBFM
from networkx import to_numpy_matrix
from networkx import from_numpy_matrix
from networkx import set_node_attributes


def interpolate_single_graph(G1, G2, t1, t2, t):
    """Интерполяция графа по двум соседним G1 и G2"""
    
    #Нормализация времени
    alpha = (t - t1) / (t2 - t1) if t2 != t1 else 0

    #Будем использовать представления графов через матрицы смежности
    A1 = to_numpy_matrix(G1)
    A2 = to_numpy_matrix(G2)
    
    #Вычисляем веса согласно WBFM и создаем новый граф по матрице смежности
    A = (1 - alpha)*A1 + alpha*A2
    G = from_numpy_matrix(A)
    
    #Распределяем вершины нового графа по сообществам
    com_dict = dict([(v, G1.nodes[v]["community"]) for v in G1])
    set_node_attributes(G, com_dict, "community")
    
    return G


def find_bounds(old_times, new_time):
    n_old = len(old_times)
    left_bound_idx, left_bound = [(i, element) for i, element in enumerate(old_times) if element <= new_time][-1]
    right_bound_idx = left_bound_idx + 1 
    right_bound_idx = right_bound_idx if right_bound_idx != n_old else left_bound_idx

    return left_bound_idx, right_bound_idx


def interpolate_time_series(old_times, old_graphs, new_times):
    """Пайплайн заполнения пропусков интерполяцией для проведения тестов"""

    new_graphs = []
    for time in new_times:
        #Для каждого момента времени в новой последовательности найдем индексы 
        #ближайших соседей, затем по индексам определим самих соседей и моменты времени
        left_bound_idx, right_bound_idx = find_bounds(old_times, time)
        G1, G2 = old_graphs[left_bound_idx], old_graphs[right_bound_idx]
        t1, t2 = old_times[left_bound_idx], old_times[right_bound_idx]

        #Найдем пропущенный граф интерполяцией
        G = interpolate_single_graph(G1, G2, t1, t2, time)

        new_graphs.append(G)
    
    return new_graphs