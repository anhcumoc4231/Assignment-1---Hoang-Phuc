"""Create or reopen the assignment's persistent SQLite database."""
from pathlib import Path
import sqlite3
import pandas as pd

COLUMNS = ('id', 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo',
           'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio')


def open_cardio_database(frame, database_path, schema_path):
    """Import once; validate existing data without replacing it on later runs."""
    if tuple(frame.columns.str.lower()) != COLUMNS:
        raise ValueError('Unexpected source columns.')
    source = frame.copy()
    source.columns = list(COLUMNS)
    source = source.sort_values('id').reset_index(drop=True)
    if len(source) != 70000 or source.id.nunique() != 70000:
        raise ValueError('Expected 70,000 unique source records.')
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='CARDIO_TRAIN'"
        ).fetchone() is not None
        if not exists:
            connection.execute('BEGIN')
            connection.execute(Path(schema_path).read_text(encoding='utf-8'))
            columns = ', '.join(c.upper() for c in COLUMNS)
            placeholders = ', '.join('?' for _ in COLUMNS)
            connection.executemany(
                f'INSERT INTO CARDIO_TRAIN ({columns}) VALUES ({placeholders})',
                source.itertuples(index=False, name=None),
            )
            connection.commit()
        stored = pd.read_sql_query('SELECT * FROM CARDIO_TRAIN ORDER BY ID', connection)
        stored.columns = stored.columns.str.lower()
        pd.testing.assert_frame_equal(stored, source, check_dtype=False)
        if connection.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('SQLite integrity check failed.')
        return connection, not exists
    except Exception:
        connection.rollback()
        connection.close()
        raise
