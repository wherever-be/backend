from dataclasses import dataclass

from chalicelib.connection import Connection


@dataclass(frozen=True)
class Journey:
    start_connection: Connection
    end_connection: Connection
