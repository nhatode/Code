class TeamsNotifier:
    def __init__(self, webhook_url: str):
        """
        Initialize Teams notifier
        Args:
            webhook_url (str): Microsoft Teams webhook URL
        """
        self.webhook_url = webhook_url
