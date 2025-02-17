from django.core.management.base import BaseCommand
from polls.models import Vote, Ranking, Subject


class Command(BaseCommand):
    help = "Convert Vote rankings from JSON field to Ranking model"

    def handle(self, *args, **kwargs):
        votes = Vote.objects.all()
        for vote in votes:
            for ranking in vote.rankings:
                order = ranking.get("order")
                subject_id = ranking.get("subject")
                try:
                    subject = Subject.objects.get(id=subject_id)
                    Ranking.objects.create(vote=vote, order=order, subject=subject)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created Ranking for Vote {vote.id}: Order {order}, Subject {subject_id}"
                        )
                    )
                except Subject.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Subject with id {subject_id} does not exist. Skipping."
                        )
                    )
