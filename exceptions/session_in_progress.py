class SessionInProgress(Exception):
    def __init__(self, session_id, message="Session with id `{}` is already in progress."):
        self.session_id = session_id
        self.message = message
        super().__init__(self.message.format(self.session_id))
