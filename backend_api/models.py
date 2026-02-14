# backend_api\models.py
"""
Domänmodellen ("vad är ett ärende?")
Syfte: Beskriva konceptet ärende i systemet.
Viktigt: Den här modellen representerar logiken, inte
vailidering.
"""

class Case:
    def __init__(self, id: int, title: str, description: str, status: str):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
