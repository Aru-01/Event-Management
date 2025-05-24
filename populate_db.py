import os
import django
import random
from faker import Faker
from django.core.files import File
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

from events.models import Category, Participant, Event

fake = Faker()

CATEGORY_DATA = [
    {
        "name": "Technology",
        "description": "Latest trends and innovations in software, hardware, AI, and startups.",
    },
    {
        "name": "Music",
        "description": "Live concerts, music festivals, and workshops with famous artists.",
    },
    {
        "name": "Art",
        "description": "Exhibitions, art fairs, painting, sculpture, and creative workshops.",
    },
    {
        "name": "Sports",
        "description": "Competitive matches, training camps, and friendly tournaments in various sports.",
    },
]

# এখানে যতগুলো ইভেন্ট বানাবে ততগুলো ইমেজের নাম থাকবে।
EVENT_IMAGES = [
    "AI-Summit.jpg",
    "Tech-Expo.jpg",
    "Startup-Meetup.jpg",
    "Developer-Conference.jpg",
    "Rock-Concert.jpg",
    "Classical-Evening.jpg",
    "Open-Mic-Night.jpg",
    "Jazz-Festival.jpg",
    "Modern-Art-Fair.jpg",
    "Art-Expo.jpg",
    "Painting-Workshop.jpg",
    "Startup-Meetup.jpg",
    "Sculpture-Showcase.jpg",
    "Yoga-Retreat.jpg",
    "Cricket-Cup.jpg",
    "Football-Tournament.jpg",
    "City-Marathon.jpg",
]


def generate_event_name(category_name):
    """Generate a realistic event name based on the category"""
    if category_name == "Technology":
        prefixes = ["AI Summit", "Tech Expo", "Developer Conference", "Startup Meetup"]
        return f"{random.choice(prefixes)} {random.randint(2024, 2026)}"
    elif category_name == "Music":
        prefixes = [
            "Jazz Festival",
            "Rock Concert",
            "Classical Evening",
            "Open Mic Night",
        ]
        return f"{random.choice(prefixes)}"
    elif category_name == "Art":
        prefixes = [
            "Art Expo",
            "Sculpture Showcase",
            "Modern Art Fair",
            "Painting Workshop",
        ]
        return f"{random.choice(prefixes)}"
    elif category_name == "Sports":
        prefixes = [
            "City Marathon",
            "Football Tournament",
            "Cricket Cup",
            "Yoga Retreat",
        ]
        return f"{random.choice(prefixes)}"
    else:
        return f"{category_name} Event {random.randint(1,100)}"


def populate_db(num_events=12):
    """
    Populate the database with categories, participants, and events.
    num_events: কতগুলো event তৈরি করবে (ডিফল্ট ১২)
    """
    # Create categories
    categories = []
    for cat in CATEGORY_DATA:
        category, created = Category.objects.get_or_create(
            name=cat["name"], defaults={"description": cat["description"]}
        )
        categories.append(category)
    print(f"✅ Created or fetched {len(categories)} categories.")

    # Create participants
    participants = []
    for _ in range(20):
        participant, created = Participant.objects.get_or_create(
            email=fake.unique.email(), defaults={"name": fake.name()}
        )
        participants.append(participant)
    print(f"✅ Created or fetched {len(participants)} participants.")

    # Check if enough images are provided
    if num_events > len(EVENT_IMAGES):
        raise ValueError(
            f"EVENT_IMAGES এ কমপক্ষে {num_events} টি ইমেজ ফাইলের নাম দিতে হবে।"
        )

    # Create events
    for i in range(num_events):
        selected_category = random.choice(categories)
        image_filename = EVENT_IMAGES[i]
        image_path = os.path.join(
            settings.BASE_DIR, "static/sample-images", image_filename
        )

        if not os.path.exists(image_path):
            print(f"⚠️ ইমেজ ফাইল পাওয়া যায়নি: {image_path}. ইভেন্ট তৈরি হচ্ছে না।")
            continue

        with open(image_path, "rb") as img_file:
            event_name = generate_event_name(selected_category.name)
            event_description = (
                fake.paragraph(nb_sentences=4)
                + f" This event focuses on {selected_category.description.lower()}."
            )

            event = Event.objects.create(
                name=event_name,
                description=event_description,
                date=fake.date_between(start_date="-30d", end_date="+30d"),
                time=fake.time(),
                location=fake.city(),
                category=selected_category,
            )
            event.img.save(image_filename, File(img_file), save=True)
            event.participants.set(random.sample(participants, k=random.randint(2, 6)))

        print(f"🎉 Created event: {event_name} with image {image_filename}")

    print("✅ Successfully populated the database!")


if __name__ == "__main__":
    populate_db()
