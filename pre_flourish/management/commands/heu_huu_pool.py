from django.core.management.base import BaseCommand

from pre_flourish.helper_classes.heu_pool_generation import HEUPoolGeneration
from pre_flourish.helper_classes.huu_pool_generation import HUUPoolGeneration


class Command(BaseCommand):
    help = "Refreshes HUU HEU matching pool."

    def handle(self, *args, **options):
        print("Generating HUU matching pool...")
        HUUPoolGeneration().generate_pool()
        print("Generating HUU matching pool...")
        HEUPoolGeneration().generate_pool()
        print("Done.🚀")
