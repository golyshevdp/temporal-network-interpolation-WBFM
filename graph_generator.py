#Генерация синтетических темпоральных сетей при помощи LFR модели
import numpy as np
from networkx.generators.community import LFR_benchmark_graph
from scipy.interpolate import interp1d


def generate_random_mu(n_snaps):
    """Функция, позволяющая генерировать случайную
     последовательность параметров смешивания для
     генерации сети с переменной модулярностью"""
    rand_mu = np.random.uniform(0.25, 0.6, 9)
    old_time = np.linspace(0, n_snaps, 9)
    time_range = list(range(n_snaps))

    #Для того, чтобы избежать большого количества скачков модулярности, 
    #сгенерируем 9 случайных точек и затем переинтерполируем
    #нашу последовательность на n_snaps точек
    f = interp1d(old_time, rand_mu)

    return f(time_range)


def assign_weights(G, random_weights=True):
    #Назначаем вновь сгенерирированному графу произвольные веса
    #флаг random_weights позволяет оставлять веса равными 1
    for edge in G.edges():
        G[edge[0]][edge[1]]['weight'] = np.random.uniform(0.0, 1.0) if random_weights else 1

    return G


def normalize_weights(G):
    #Нормализация весов для вновь сгенерированного графа
    m = np.sum([edge[2]['weight'] for edge in G.edges(data=True)])

    for edge in G.edges(data=True):
        edge[2]['weight'] = edge[2]['weight'] / m

    return G


def generate_time_series(mu_range, n=100, random_weights=True, normalize_weights_flag=True):
    """Весь пайплайн генерации синтетической сети"""

    #константы для LFR
    tau1 = 2.0
    tau2 = 1.5
    avg_degree = 5
    min_comm = 40

    #Итеративно изменяем параметр смешивания и генерируем 
    #графы с переменной модулярностью
    graphs = []
    for mu in mu_range:
        G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=avg_degree, min_community=min_comm, seed=10)
        
        G = assign_weights(G, random_weights)
        
        if normalize_weights_flag:
            G = normalize_weights(G)

        graphs.append(G)

    return graphs