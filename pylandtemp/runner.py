class Runner:
    def __init__(self, methods):
        """
        Task and method agnostic runner

        args:
        methods (dict): dictionary that maps defined keys to concrete algorithimic implementations of the called method.
        """

        self.methods = methods

    def __call__(self, method, **kwargs):

        compute_method = self._get_method(method)

        return compute_method()(**kwargs)

    def _get_method(self, method):

        if method not in self.methods:
            raise ValueError(
                f"Requested method not implemented. Choose among available methods: {list(self.methods.values())}"
            )

        return self.methods.get(method)
