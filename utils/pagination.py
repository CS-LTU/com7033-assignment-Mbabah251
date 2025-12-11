def get_paginated_patients(page=1, per_page=10):
    """
    Get paginated patients from database.
    Returns dict with patients, total count, and pagination info.
    """
    import sqlite3

    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) as count FROM patients")
    total = cursor.fetchone()['count']

    # Calculate offset
    offset = (page - 1) * per_page

    # Get paginated patients
    cursor.execute(
        "SELECT * FROM patients ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (per_page, offset)
    )
    patients = cursor.fetchall()
    conn.close()

    # Calculate total pages
    total_pages = (total + per_page - 1) // per_page

    return {
        'patients': patients,
        'current_page': page,
        'total_pages': total_pages,
        'total_count': total,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page < total_pages,
    }
