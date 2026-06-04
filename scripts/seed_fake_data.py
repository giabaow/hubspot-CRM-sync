"""
Seed the local PostgreSQL database with fake CRM data for testing.
Run: python scripts/seed_fake_data.py
"""
from faker import Faker
from app.core.database import SessionLocal, init_db
from app.models.contact import Contact
from app.models.deal import Deal
import random

fake = Faker()

DEAL_STAGES = ["appointmentscheduled", "qualifiedtobuy", "presentationscheduled", "decisionmakerboughtin", "contractsent", "closedwon", "closedlost"]


def seed(n_contacts=50, n_deals=30):
    init_db()
    db = SessionLocal()

    for i in range(n_contacts):
        db.add(Contact(
            hubspot_id=f"fake-{1000 + i}",
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.email(),
            company=fake.company(),
            phone=fake.phone_number(),
        ))

    for i in range(n_deals):
        db.add(Deal(
            hubspot_id=f"fake-deal-{2000 + i}",
            dealname=f"{fake.bs().title()} Deal",
            amount=round(random.uniform(1000, 100000), 2),
            dealstage=random.choice(DEAL_STAGES),
            closedate=fake.date_this_year().isoformat(),
            pipeline="default",
        ))

    db.commit()
    db.close()
    print(f"Seeded {n_contacts} contacts and {n_deals} deals.")


if __name__ == "__main__":
    seed()
