class RequiredSecretNotFound(Exception):
    """
    Exception raised when a required secret is not found.
    """

    def __init__(self, secret_id: str):
        """
        Initialize the RequiredSecretNotFound exception.

        Args:
            secret_id (str): The ID of the secret that was not found.
        """
        super().__init__(f"Required secret not found: {secret_id}")
