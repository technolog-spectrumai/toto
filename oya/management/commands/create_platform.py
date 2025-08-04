from django.core.management.base import BaseCommand
from oya.models import Platform, Company, TLSCertificate, Theme  # Adjust imports if needed
from datetime import datetime


class Command(BaseCommand):
    help = "Create a Platform instance with company reference, TLS certificate, optional theme, and publication year inferred from execution"

    def add_arguments(self, parser):
        parser.add_argument('site_name', type=str, help='Platform site name')
        parser.add_argument('domain', type=str, help='Domain name for the platform')
        parser.add_argument('company_id', type=int, help='ID of the associated Company')
        parser.add_argument('tls_certificate_id', type=int, help='ID of the TLS Certificate')
        parser.add_argument('--theme_id', type=int, help='Optional Theme ID for visual configuration')
        parser.add_argument('--active', type=bool, default=True, help='Is the platform active?')

    def handle(self, *args, **options):
        site_name = options['site_name']
        domain = options['domain']
        company_id = options['company_id']
        tls_certificate_id = options['tls_certificate_id']
        theme_id = options.get('theme_id', None)
        active = options['active']
        publication_year = datetime.now().year

        # Fetch Company
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Company with ID {company_id} not found."))
            return

        # Fetch TLS Certificate
        try:
            tls_certificate = TLSCertificate.objects.get(id=tls_certificate_id)
        except TLSCertificate.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"TLS Certificate with ID {tls_certificate_id} not found."))
            return

        # Fetch Theme (optional)
        theme = None
        if theme_id:
            try:
                theme = Theme.objects.get(id=theme_id)
            except Theme.DoesNotExist:
                self.stderr.write(self.style.WARNING(f"Theme with ID {theme_id} not found — continuing without theme."))

        # Create or Update Platform
        platform, created = Platform.objects.update_or_create(
            domain=domain,
            site_name=site_name,
            company=company,
            defaults={
                "publication_year": publication_year,
                "active": active,
                "tls_certificate": tls_certificate,
                "theme": theme
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Platform: {platform.site_name} for {company.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated Platform: {platform.site_name} for {company.name}"))
