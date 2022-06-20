#Кастомное вычисление модулярности для оптимизации последующих вычислений
from networkx import to_numpy_matrix
import numpy as np


def if_in_similar_community(communities, i, j):
    """Проверка того, что узлы i и j лежат в одном сообществе"""
    for community in communities:
        if {i, j}.issubset(community):
            return 1
    return 0


def calculate_delta(communities, n):
    """Заполняем матрицу значений дельта"""
    delta = np.zeros(shape=(n, n))
    
    for i in range(n):
        for j in range(n):
            delta[i, j] = if_in_similar_community(communities, i, j)
    
    return delta


def calculate_k(A, n):
    """Вычисление степеней всех узлов по матрице смежности"""
    k = np.zeros(n)
    
    for i in range(n):
        k[i] = np.sum([A[i, j] for j in range(n) if i != j])
    
    return k


def calculate_Q(A, k, n, delta, m=1):
    """Вычисление модулярности по известным значениям k, delta и m"""

    Q = 0
    for i in range(n):
        for j in range(n):
            Q += (A[i, j] - 1/m*0.5*k[i]*k[j]) * delta[i, j]
    
    Q = 1/m * 0.5 * Q
    
    return Q


def custom_modularity(G):
    """Весь пайплайн вычисления модулярности"""
    communities = {frozenset(G.nodes[v]["community"]) for v in G}
    
    A = to_numpy_matrix(G)
    n = A.shape[0]
    
    delta = calculate_delta(communities, n)
    k = calculate_k(A, n)
    
    m = np.sum([edge[2]['weight'] for edge in G.edges(data=True)])
    
    return calculate_Q(A, k, n, delta, m)


def calculate_differential_modularity(G1, G2, alpha):
    """Весь пайплайн вычисления дифференциальной модулярности"""
    communities = {frozenset(G1.nodes[v]["community"]) for v in G1}
    
    A1 = to_numpy_matrix(G1)
    A2 = to_numpy_matrix(G2)
    
    n = A1.shape[0]    
    delta = calculate_delta(communities, n)
    
    k1 = calculate_k(A1, n)
    k2 = calculate_k(A2, n)
    
    
    Q = 0
    for i in range(n):
        for j in range(n):
            Q += (k1[i] - k2[i])*(k1[j] - k2[j]) * delta[i, j]
    
    Q = alpha * (1-alpha) * 0.25 * Q
    
    return Q