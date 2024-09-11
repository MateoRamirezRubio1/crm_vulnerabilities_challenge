class AlertSubject:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlertSubject, cls).__new__(cls)
            cls._instance._observers = []  # Inicializa la lista de observadores
            cls._instance._state = None  # Estado del Subject
        return cls._instance

    def attach(self, observer):
        """Añade un observador a la lista"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Elimina un observador de la lista"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Notifica a todos los observadores"""
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, alert_severity, recipient, message):
        """Actualiza el estado y notifica a los observadores"""
        self._state = {
            "severity": alert_severity,
            "recipient": recipient,
            "message": message,
        }
        self.notify()
