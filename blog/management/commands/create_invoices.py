import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from tqdm import tqdm

from blog.models import Invoice, Organization


class Command(BaseCommand):
    help = "Create N invoices for the first available organization"

    def add_arguments(self, parser):
        parser.add_argument(
            "-q",
            "--quantity",
            type=int,
            default=4,
            help="Number of invoices to create (default: 4)",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Remove the first existing organization before creating invoices",
        )

    def handle(self, *args, **options):
        quantity = options["quantity"]

        organization = Organization.objects.first()
        if options["clean"] and organization:
            organization_name = organization.name
            organization.delete()
            self.stdout.write(f"Deleted existing organization: {organization_name}")
            organization = None

        if not organization:
            organization = Organization.objects.create(name="First Organization")
            self.stdout.write(f"Created new organization: {organization.name}")

        today = timezone.now().date()

        for _ in tqdm(range(quantity), desc="Creating invoices"):
            total_cents = random.randint(1000, 500000)
            issued_days_ago = random.randint(0, 120)
            Invoice.objects.create(
                organization=organization,
                total=Decimal(total_cents) / Decimal("100"),
                issued_at=today - timedelta(days=issued_days_ago),
            )

        self.stdout.write(
            self.style.SUCCESS(f"Created {quantity} invoices for '{organization.name}'")
        )
