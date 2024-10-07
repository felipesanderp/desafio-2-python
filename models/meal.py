"""Meal model"""

from sqlalchemy.orm import relationship
from database import db


class Meal(db.Model):
    """Meal class"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    inside_diet = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="meals")

    def get_id(self):
        """Return meal id"""
        return self.id

    def to_dict(self):
        """Format meal return"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "inside_diet": self.inside_diet,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
