


class EventDispatcher:
    def __init__(self):
        self.event_listeners = {}

    @classmethod
    def create_listener_for_id(cls, expected_id, raw_listener, **kwargs):
        def listener(id=None, **payload):
            if id == expected_id:
                return raw_listener(**kwargs, **payload)
        return listener

    def add_event_listener(self, event, listener, keep_listener, **kwargs):
        if event not in self.event_listeners:
            self.event_listeners[event] = []
        self.event_listeners[event].append((listener, keep_listener, kwargs))

    def emit(self, event, **payload):
        listeners = self.event_listeners.get(event)

        if not listeners:
            return

        for elements in listeners.copy():
            listener, keep_listener, listener_kwargs = elements
            listener(**listener_kwargs, **payload)
            if not keep_listener:
                listeners.remove(elements)

        if not listeners:
            del self.event_listeners[event]



