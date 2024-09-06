# coding: utf-8
def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    # config.add_route('bookings', '/bookings')
    # config.add_route('bookings_retrieve', '/bookings/{book_ref}')
    # config.add_route('bookings_put', '/bookings/{book_ref}')
    # config.add_route('bookings_post', '/bookings/')
    # config.add_route('bookings_delete', '/bookings/{book_ref}')


