from seed import paginate_users

def lazy_paginate(page_size):
    """Generator to lazily load paginated data from user_data table."""
    offset = 0
    # Single loop to fetch pages
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop if no more data
            break
        yield page
        offset += page_size
