from datetime import datetime as dt

from yacut.constants import MODEL_API_FIELDS
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        for field in MODEL_API_FIELDS:
            if field in data:
                print(field, data[field])
                setattr(self, field, data[field])
