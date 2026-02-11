
def is_order_expired(order_timestamp, expiration_time, current_timestamp):
    return current_timestamp - order_timestamp > expiration_time