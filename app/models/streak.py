from datetime import date
from app.extensions import db


class Streak(db.Model):
    __tablename__ = "streaks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_completed_date = db.Column(db.Date)

    last_warning_shown_date = db.Column(db.Date)
    last_kill_shown_date = db.Column(db.Date)

    user = db.relationship("User", backref=db.backref("streak", uselist=False))

    def register_completion(self):
        """Call on video completion. Only touches streak-day tracking —
        never VideoProgress."""
        today = date.today()

        if self.last_completed_date == today:
            return False

        if self.current_streak is None:
            self.current_streak = 0
        if self.longest_streak is None:
            self.longest_streak = 0

        if self.last_completed_date is not None and (today - self.last_completed_date).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1

        self.longest_streak = max(self.longest_streak, self.current_streak)
        self.last_completed_date = today
        return True

    def check_daily_status(self):
        """Call on dashboard load. Detects missed days and returns
        'warning', 'killed', 'grieving', or None. Resets current_streak
        to 0 exactly once (the 'killed' moment) — never touches
        VideoProgress, so completed videos are never undone."""
        today = date.today()

        if self.last_completed_date is None:
            return None  # never started yet

        gap = (today - self.last_completed_date).days

        if gap <= 1:
            return None

        if gap == 2:
            if self.last_warning_shown_date != today:
                self.last_warning_shown_date = today
                db.session.commit()
                return "warning"
            return None

        if self.current_streak != 0:
            self.current_streak = 0
            self.last_kill_shown_date = today
            db.session.commit()
            return "killed"

        return "grieving"

    @property
    def egg_stage(self):
        if self.current_streak >= 7:
            return "hatched"
        elif self.current_streak >= 3:
            return "cracking"
        else:
            return "intact"

    def __repr__(self):
        return f"<Streak user_id={self.user_id} current={self.current_streak}>"
