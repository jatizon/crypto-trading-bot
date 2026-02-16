import inspect


class EventDispatcher:
    def __init__(self):
        self.event_listeners = {}

    def wrap_listener(self, expected_id, raw_listener):
        has_order_id = "order_id" in inspect.signature(raw_listener).parameters
        def listener(order_id, **payload):
            run = (order_id == expected_id) if expected_id is not None else True

            if not run:
                return run, None

            if has_order_id:
                return run, raw_listener(order_id, **payload)
            else:
                return run, raw_listener(**payload)
        return listener

    def add_event_listener(self, event, listener, keep_listener, expected_id=None, static_payload=None):
        wrapped_listener = self.wrap_listener(expected_id, listener)

        if static_payload is None:
            static_payload = {}

        if event not in self.event_listeners:
            self.event_listeners[event] = []
        self.event_listeners[event].append((wrapped_listener, keep_listener, static_payload))

    def emit(self, event, order_id=None, event_payload=None):
        if event_payload is None:
            event_payload = {}

        listeners = self.event_listeners.get(event)

        if not listeners:
            return
            
        outputs = []

        for elements in listeners.copy():
            listener, keep_listener, static_payload = elements

            merged_payload = {**event_payload, **static_payload}
            
            ran, output = listener(order_id, **merged_payload)
            if ran:
                outputs.append(output)
            if ran and not keep_listener:
                    listeners.remove(elements)

        if not listeners:
            del self.event_listeners[event]

        return outputs


