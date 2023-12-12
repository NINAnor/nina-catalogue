from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class DataReportPage(Page):
    subtitle = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    number = models.TextField(blank=True, null=True, verbose_name="Report number")
    isbn = models.TextField(blank=True, null=True)

    summary = RichTextField(blank=True, null=True, max_length=4000)

    place = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField(blank=True, null=True)

    keywords = models.TextField(blank=True)

    metadata_introduction = RichTextField(blank=True, null=True)
    metadata_datastructure = RichTextField(blank=True, null=True)
    metadata_geografic_definition = models.TextField(blank=True, null=True)
    metadata_taxonomy = models.TextField(blank=True, null=True)
    metadata_timerange_start = models.DateTimeField(blank=True, null=True)
    metadata_timerange_end = models.DateTimeField(blank=True, null=True)
    metadata_collection_methods = RichTextField(blank=True, null=True)
    metadata_study_scope = models.TextField(blank=True, null=True)
    metadata_study_description = models.TextField(blank=True, null=True)
    metadata_qc = models.TextField(blank=True, null=True)

    data = RichTextField(blank=True, null=True)
    guidelines = RichTextField(blank=True, null=True)
    additional_info = RichTextField(blank=True, null=True)
    references = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("number", permission="reports.change_publishing_fields"),
        FieldPanel("isbn", permission="reports.change_publishing_fields"),
        FieldPanel("authors"),
        FieldPanel("date"),
        FieldPanel("place"),
        FieldPanel("keywords"),
        FieldPanel("summary"),
        FieldPanel("metadata_introduction"),
        FieldPanel("metadata_datastructure"),
        FieldPanel("metadata_geografic_definition"),
        FieldPanel("metadata_taxonomy"),
        FieldPanel("metadata_timerange_start"),
        FieldPanel("metadata_timerange_end"),
        FieldPanel("metadata_collection_methods"),
        FieldPanel("metadata_study_scope"),
        FieldPanel("metadata_study_description"),
        FieldPanel("metadata_qc"),
        FieldPanel("data"),
        FieldPanel("guidelines"),
        FieldPanel("additional_info"),
        FieldPanel("references"),
    ]

    parent_page_types = ["DataReportsIndexPage"]
    subpage_types = []

    class Meta:
        permissions = [
            ("change_publishing_fields", "Can change the fields related to publishing"),
        ]


class DataReportsIndexPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Landscape mode only; horizontal width between 1000px and " "3000px.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("image"),
    ]

    subpage_types = ["DataReportPage"]
    parent_page_types = ["cms.HomePage"]
    max_count_per_parent = 1

    # Returns a queryset of DataReportPage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_reports(self):
        return DataReportPage.objects.live().descendant_of(self).order_by("-first_published_at")

    # Allows child objects (e.g. DataReportPage objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get("page")
        paginator = Paginator(self.get_reports(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super().get_context(request)
        reports = self.paginate(request, self.get_reports())
        context["reports"] = reports
        return context
