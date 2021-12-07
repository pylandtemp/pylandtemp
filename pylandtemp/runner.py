class Runner:
    def __init__(self, algorithms):
        """
        Task and method agnostic runner

        args:
        algorithms (dict): dictionary that maps defined keys to concrete implementations of the called algorithm.
        """
        self.algorithms = algorithms

    def __call__(self, method, **kwargs):
        compute_algorithm = self._get_algorithm(method)
        return compute_algorithm()(**kwargs)

    def _get_algorithm(self, algo):
        if algo not in self.algorithms:
            raise ValueError(
                f"Requested method not implemented. Choose among available methods: {list(self.algorithms.values())}"
            )
        return self.algorithms[algo]
