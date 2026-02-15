
import inspect

class EventDispatcher:
    def __init__(self):
        self.event_listeners = {}

    @staticmethod
    def create_listener_for_id(expected_id, raw_listener, **kwargs):
        accepts_id = 'id' in inspect.signature(raw_listener).parameters

        def listener(id, **payload):
            run = (id == expected_id)
            if not run:
                return run, None
            if accepts_id:
                return run, raw_listener(id=id, **kwargs, **payload)
            return run, raw_listener(**kwargs, **payload)
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
            ran, _ = listener(**listener_kwargs, **payload)
            if not keep_listener and ran:
                listeners.remove(elements)

        if not listeners:
            del self.event_listeners[event]



