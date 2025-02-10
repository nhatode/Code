class ServiceNowTicket:
    def __init__(self, ticket_number: str, description: str, priority: str, 
                 assigned_to: str, status: str):
        """
        Initialize ServiceNow ticket information
        """
        self.ticket_number = ticket_number
        self.description = description
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = status
