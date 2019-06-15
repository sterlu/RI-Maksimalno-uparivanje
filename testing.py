import matplotlib.pyplot as plt
import numpy as np
import time

from utils import draw_graph, create_graph


def test(search_fs, edges=10, nodes=10, draw=True):
    print('Creating graph')
    graph = create_graph(edges, nodes)

    for search_f in search_fs:
        print()
        print('Testing', search_f.__name__)
        start = time.time()

        result = search_f(graph)

        end = time.time()
        print('{3} with {0} nodes and {1} edges took {2:.3f}s'.format(nodes, edges, end - start, search_f.__name__))
        print('Final result', result)

        if draw:
            draw_graph(graph)

        for (v, w) in graph.edges:
            graph[v][w]['in_matching'] = False


def compare(search_f_1, search_f_2, edges=10, nodes=10, iterations=100):
    print('Comparing {0} and {1}'.format(search_f_1.__name__, search_f_2.__name__))
    results = {
        search_f_1.__name__: 0,
        search_f_2.__name__: 0,
        'equal': 0
    }
    for i in range(0, iterations):
        graph = create_graph(edges, nodes)
        res_1 = search_f_1(graph)
        res_2 = search_f_2(graph)

        if res_1 < res_2:
            results[search_f_1.__name__] += 1
        elif res_2 < res_1:
            results[search_f_2.__name__] += 1
        else:
            results['equal'] += 1
    print(results)


def detailed_compare(search_fs, edges=10, nodes=10, iterations=100, plot=False):
    results = {}
    sums = {}
    for search_f in search_fs:
        results[search_f.__name__] = []
        sums[search_f.__name__] = 0
    for i in range(0, iterations):
        graph = create_graph(edges, nodes)
        for search_f in search_fs:
            res = search_f(graph)
            results[search_f.__name__].append(res)
            sums[search_f.__name__] += res
    plt.figure(figsize=(8, 6))
    ax = plt.subplot(111)
    if plot:
        for search_f in search_fs:
            line, = ax.plot(
                range(1, iterations + 1),
                results[search_f.__name__]
            )
            line.set_label(search_f.__name__)
        ax.set_ylim(bottom=0)
        plt.title('{0} čvorova/{1} ivica'.format(nodes, edges))
    else:
        averages = []
        _averages = {}
        for search_f in search_fs:
            name = search_f.__name__
            averages.append(sums[name] / iterations)
            print(name, averages[-1])
            _averages[name] = averages[-1]
            plt.bar([name], averages[-1], zorder=10)
        plt.grid(True, which='both', axis='y', zorder=0, alpha=1)
        plt.grid(which='minor', alpha=.3)
        major_ticks = np.arange(0, max(averages) + 1, 5)
        minor_ticks = np.arange(0, max(averages) + 1, 1)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)
        plt.legend(list(map(lambda f: f.__name__ + ' ' + str(_averages[f.__name__]), search_fs)), loc='upper center', bbox_to_anchor=(0.5, -0.05))
        plt.tick_params(axis='x', bottom=False, labelbottom=False)
        plt.title('Prosek za {0} čvorova/{1} ivica u {2} iteracija\n'.format(nodes, edges, iterations))
        plt.suptitle('\n\n(manje je bolje)', fontsize=8)
    plt.show()


def compare_iterations(search_f, edges=10, nodes=10, iterations=100):
    results = []
    graph = create_graph(edges, nodes)
    for i in range(1, iterations + 1):
        results.append(search_f(graph, iterations=i))
    print(results)
    plt.figure(figsize=(12, 6))
    ax = plt.subplot(111)
    ax.plot(results)
    plt.grid(True, which='both', axis='y', zorder=0, alpha=1)
    major_ticks = np.arange(min(results)-1, max(results)+1, 1)
    ax.set_yticks(major_ticks)
    plt.title(search_f.__name__ + ' - Rezultati po broju iteracija\n\n')
    plt.suptitle('\n\n{0} čvorova/{1} ivica do {2} iteracija\n(manje je bolje)'.format(nodes, edges, iterations), fontsize=8)
    plt.show()
