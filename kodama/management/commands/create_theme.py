from django.core.management.base import BaseCommand
from kodama.models import Theme, Font


STRUCTURAL_CLASSES = {
    "light": {
        "body": "bg-gray-100 text-gray-900",
        "header": "bg-gradient-to-r from-blue-400 to-green-500",
        "footer": "bg-blue-100",
        "navbar_wrapper": "",
        "navbar_title": "text-gray-800",
        "nav_link": "text-gray-800",
        "nav_dropdown": "bg-gray-100 border-gray-300 text-gray-900 shadow-md",
        "toggle_button": "bg-green-600 text-white border-green-800 hover:bg-green-700",
        "mobile_nav_panel": "bg-white text-gray-800",
        "latest_intro": "text-gray-700 text-sm text-center mb-4",
        "login_box": "bg-white text-gray-900 border-gray-300 shadow transition",
        "login_title": "text-green-700",
        "login_input": "bg-white text-black border-green-800 placeholder-gray-600 focus:ring-green-700",
        "login_button": "bg-green-700 border-green-900 text-white hover:bg-green-800",
        "login_link": "text-blue-600 hover:underline",
        "profile_wrapper": "bg-white text-gray-900 shadow-lg rounded-lg overflow-hidden",
        "profile_field_label": "text-gray-600 text-sm font-medium",
        "profile_field_value": "text-gray-900 text-lg",
        "profile_divider": "divide-gray-200",
        "profile_footer": "bg-gray-100 text-gray-800 hover:bg-gray-200 border-t border-gray-200",
        "search_intro_text": "text-gray-700 text-sm text-center mb-4",
        "search_empty_text": "text-gray-500 text-sm text-center",
        "tag_title": "text-gray-900 text-center",
        "tag_intro": "text-gray-700 text-sm text-center mb-4",
        "tag_empty_text": "text-gray-500 text-sm text-center",
        "source_card": "bg-white text-gray-900 border-gray-300 shadow transition",
        "company_card": "bg-white text-gray-900 border-gray-300 shadow transition",
        "source_detail_box": "bg-white text-gray-900 shadow-lg rounded-lg overflow-hidden",
        "source_divider": "divide-gray-200",
        "source_field_label": "text-gray-600",
        "source_field_value": "text-gray-900",
        "source_back_button": "bg-gray-100 text-gray-800 hover:bg-gray-200",
        "section_title": "text-gray-800",
        "footer_link": "text-blue-800 hover:text-blue-900",
        "footer_notice": "text-gray-700 border-gray-300",
        "search_field": "bg-transparent border-green-800 text-black placeholder-gray-600 focus:ring-green-700",
        "search_submit": "bg-green-700 border-green-900 text-white hover:bg-green-800",
        "draft_badge": "bg-green-100 hover:bg-green-200 text-green-800 border-green-600",
        "meta_text": "text-gray-500",
        "image_border": "border border-gray-300",
        "image_caption": "text-gray-600",
        "author_link": "text-blue-700 hover:underline",
        "edit_button": "bg-blue-100 hover:bg-blue-200 text-blue-800 border border-blue-200",
        "category_badge": "bg-gray-200 text-gray-800",
        "abstract_box": "border border-gray-300 bg-white text-gray-900",
        "content_box": "border border-gray-200 bg-white text-gray-900",
        "tag_link": "bg-blue-100 text-blue-800 hover:bg-blue-200",
        "home_link": "text-gray-700 hover:underline",
        "like_button": "text-green-600 hover:text-green-700",
        "like_count_text": "text-green-700",
        "dislike_button": "text-red-600 hover:text-red-700",
        "dislike_count_text": "text-red-700",
        "section_divider": "border-gray-300",
        "category_link": "text-blue-800 hover:text-blue-900",
        "source_link": "text-blue-800 hover:text-blue-900",
        "email_link": "text-blue-800 hover:text-blue-900",
        "profile_back_button": "bg-gray-100 text-gray-800 hover:bg-gray-200",
        "library_link": 'bg-blue-100 hover:bg-blue-200 text-blue-800',
        "section_body": "p-2"
    },
    "dark": {
        "body": "bg-gray-900 text-gray-100",
        "header": "bg-gradient-to-r from-gray-800 to-gray-900",
        "footer": "bg-gray-800",
        "navbar_wrapper": "",
        "navbar_title": "text-blue-400",
        "nav_link": "text-gray-300",
        "nav_dropdown": "bg-gray-900 border-gray-700 text-gray-100 shadow-black",
        "toggle_button": "bg-gray-700 text-gray-300 border-gray-500 hover:bg-gray-600",
        "mobile_nav_panel": "bg-gray-800 text-gray-300",
        "latest_intro": "text-gray-400 text-sm text-center mb-4",
        "login_box": "bg-gray-800 text-white border-gray-600 shadow transition",
        "login_title": "text-blue-300",
        "login_input": "bg-gray-700 text-white border-blue-500 placeholder-blue-200 focus:ring-blue-500",
        "login_button": "bg-blue-700 border-blue-500 text-white hover:bg-blue-600",
        "login_link": "text-blue-300 hover:underline",
        "profile_wrapper": "bg-gray-800 text-gray-100 shadow-lg rounded-lg overflow-hidden",
        "profile_field_label": "text-gray-400 text-sm font-medium",
        "profile_field_value": "text-gray-100 text-lg",
        "profile_divider": "divide-gray-700",
        "profile_footer": "bg-gray-700 text-gray-200 hover:bg-gray-600 border-t border-gray-700",
        "search_intro_text": "text-gray-400 text-sm text-center mb-4",
        "search_empty_text": "text-gray-400 text-sm text-center",
        "tag_title": "text-gray-100 text-center",
        "tag_intro": "text-gray-400 text-sm text-center mb-4",
        "tag_empty_text": "text-gray-400 text-sm text-center",
        "source_card": "bg-gray-800 text-white border-gray-600 shadow transition",
        "company_card": "bg-gray-800 text-white border-gray-600 shadow transition",
        "source_detail_box": "bg-gray-800 text-gray-100 shadow-lg rounded-lg overflow-hidden",
        "source_divider": "divide-gray-700",
        "source_field_label": "text-gray-400",
        "source_field_value": "text-gray-100",
        "source_back_button": "bg-gray-700 text-gray-200 hover:bg-gray-600",
        "section_title": "text-gray-300",
        "footer_link": "text-blue-400 hover:text-blue-500",
        "footer_notice": "text-gray-500 border-gray-700",
        "search_field": "bg-transparent border-blue-500 text-white placeholder-blue-200 focus:ring-blue-500",
        "search_submit": "bg-blue-700 border-blue-500 text-white hover:bg-blue-600",
        "draft_badge": "bg-gray-700 hover:bg-gray-600 text-green-300 border-green-300",
        "meta_text": "text-gray-400",
        "image_border": "border border-gray-700",
        "image_caption": "text-gray-400",
        "author_link": "text-blue-300 hover:underline",
        "edit_button": "bg-gray-700 hover:bg-gray-600 text-white border-gray-600",
        "category_badge": "bg-gray-700 text-gray-100",
        "abstract_box": "border border-gray-600 bg-gray-900 text-gray-100",
        "content_box": "border border-gray-600 bg-gray-900 text-gray-100",
        "tag_link": "bg-gray-700 text-gray-200 hover:bg-gray-600",
        "home_link": "text-blue-300 hover:underline",
        "like_button": "text-green-400 hover:text-green-300",
        "like_count_text": "text-green-300",
        "dislike_button": "text-red-400 hover:text-red-300",
        "dislike_count_text": "text-red-300",
        "section_divider": "border-gray-600",
        "category_link": "text-blue-400 hover:text-blue-500",
        "source_link": "text-blue-400 hover:text-blue-500",
        "email_link": "text-blue-400 hover:text-blue-500",
        "profile_back_button": "bg-gray-700 text-gray-200 hover:bg-gray-600",
        "library_link": 'bg-blue-700 hover:bg-blue-600 text-white',
        "section_body": "p-2",
    }
}





class Command(BaseCommand):
    help = "Generates a Theme with Tailwind classes for structural elements"

    def add_arguments(self, parser):
        parser.add_argument(
            "name",
            type=str,
            help="Theme name"
        )

    def _create_fonts(self):
        font_data = {
            "Playfair Display": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap",
            "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
        }

        fonts = {}
        for name, link in font_data.items():
            font, _ = Font.objects.get_or_create(
                name=name,
                defaults={"cdn_link": link}
            )
            fonts[name] = font

        return fonts


    def handle(self, *args, **options):

        fonts = self._create_fonts()
        default_font = fonts[list(fonts.keys())[0]]

        theme_name = options["name"]
        tokens = []

        schema = Theme.SCHEMA["items"]["properties"]
        elements = schema["element"]["enum"]
        modes = schema["mode"]["enum"]

        for mode in modes:
            for element in elements:
                cls = STRUCTURAL_CLASSES.get(mode, {}).get(element)
                if cls:
                    tokens.append({
                        "element": element,
                        "mode": mode,
                        "class": cls
                    })

        theme = Theme.objects.create(
            name=theme_name,
            theme=tokens,
            font=default_font
        )

        self.stdout.write(self.style.SUCCESS(
            f"Theme '{theme.name}' created with {len(tokens)} structural tokens."
        ))
