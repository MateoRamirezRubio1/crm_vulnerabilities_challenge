import logging

logger = logging.getLogger("alerts")


class AlertSubject:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertSubject, cls).__new__(cls)
            cls._instance._observers = []  # Initialize the list of observers
            cls._instance._state = None  # State of the Subject
        return cls._instance

    def attach(self, observer):
        """Adds an observer to the list."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observer {observer} attached.")

    def detach(self, observer):
        """Removes an observer from the list."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observer {observer} detached.")

    def notify(self):
        """Notifies all observers."""
        for observer in self._observers:
            try:
                observer.update(self._state)
                logger.info(f"Notified observer {observer} with state {self._state}.")
            except Exception as e:
                logger.error(f"Failed to notify observer {observer}: {e}")

    def set_state(self, alert_severity: str, recipient: str, message: str):
        """Updates the state and notifies the observers."""
        self._state = {
            "severity": alert_severity,
            "recipient": recipient,
            "message": message,
        }
        logger.info(f"State updated to {self._state}. Notifying observers.")
        self.notify()
