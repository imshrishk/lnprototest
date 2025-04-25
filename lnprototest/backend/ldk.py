from .backend import Backend
from ..dummyrunner import DummyRunner

class LDKNodeRunner(DummyRunner):
    """
    LDK Node Runner for lnprototest.
    
    This is a placeholder implementation that extends DummyRunner.
    In a real implementation, this would interact with a running LDK node.
    """

    def __init__(self, config=None):
        # Initialize with dummy config for now
        super().__init__(config)
        self.is_ldk = True
    
    def start(self):
        """Start the LDK node."""
        # In a real implementation, this would start the LDK node
        super().start()
        
    def stop(self, print_logs=False):
        """Stop the LDK node."""
        # In a real implementation, this would stop the LDK node
        super().stop(print_logs)
        
    def get_node_privkey(self) -> str:
        """Return the node private key."""
        # In a real implementation, this would return the actual node private key
        return "02" * 32
    
    def has_option(self, optname: str) -> str:
        """Check if the node has a specific option."""
        # Return special options for LDK specifically
        if optname == "supports_ldk":
            return "yes"
        return super().has_option(optname)
