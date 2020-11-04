import django_filters
from .models import JobOpp

class JobOppFilter(django_filters.FilterSet):

    ORDER_CHOICES = [
        ('desc', 'Newest'),
        ('asc', 'Oldest')
    ]

    order_by = django_filters.ChoiceFilter(label='Order By', choices=ORDER_CHOICES, method='filter_order')

    def __init__(self, *args, **kwargs):
        super(JobOppFilter, self).__init__(*args, **kwargs)
        self.filters['age_wanted'].label = 'Age'
        self.filters['is_paid'].label = 'Paid'

    class Meta:
        model = JobOpp
        fields = ['location',
                  'language',
                  'gender',
                  'age_wanted',
                  'is_paid',
                  'from_home']

        field_name = {
            'age_wanted': 'User account',
        }

    def filter_order(self, queryset, name, value):
        expression = 'posted_at' if value == 'asc' else '-posted_at'
        return queryset.order_by(expression)
