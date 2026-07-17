"""
Factory Boy factories for HCP module test data.
Used across all test modules to generate realistic model instances.
"""
import datetime
import factory
from factory.django import DjangoModelFactory

from apps.hcp.models import HealthcareProfessional, Interaction


class HealthcareProfessionalFactory(DjangoModelFactory):
    """Generates realistic HCP instances for tests."""

    class Meta:
        model = HealthcareProfessional

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    specialty = factory.Iterator([
        "Cardiology", "Oncology", "Neurology", "Endocrinology",
        "Rheumatology", "Pulmonology", "Gastroenterology", "Dermatology",
    ])
    email = factory.LazyAttribute(
        lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@hospital.com"
    )
    phone = factory.Faker("phone_number")
    institution = factory.Faker("company")


class InteractionFactory(DjangoModelFactory):
    """Generates realistic Interaction instances for tests."""

    class Meta:
        model = Interaction

    hcp = factory.SubFactory(HealthcareProfessionalFactory)
    interaction_type = factory.Iterator([
        Interaction.InteractionType.IN_PERSON,
        Interaction.InteractionType.PHONE,
        Interaction.InteractionType.VIRTUAL,
    ])
    log_method = factory.Iterator([
        Interaction.LogMethod.FORM,
        Interaction.LogMethod.CHAT,
    ])
    date = factory.LazyFunction(datetime.date.today)
    notes = factory.Faker("paragraph")
    products_discussed = factory.LazyFunction(lambda: ["DrugA", "DrugB"])
    follow_up_required = False
    follow_up_date = None
    created_by = factory.Faker("name")
