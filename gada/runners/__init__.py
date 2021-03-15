__all__ = ["RunnerBase"]
from abc import ABC, abstractmethod


class RunnerBase(ABC):
    @abstractmethod
    def run(self, component, node_config, options):
        """Run a node.

        :param component: loaded component
        :param node_config: node configuration
        :param options: run options
        :return: outputs
        """
        raise NotImplementedError()
