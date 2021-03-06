from django.conf.urls import patterns, url

from dtrcity.views import (
    city_autocomplete_crc, cities_in_country, all_countries
)


urlpatterns = patterns(
    '',
    url(r'all-countries.json$',
        all_countries, name='all_countries'),
    url(r'autocomplete-crc.json$',
        city_autocomplete_crc, name='city_autocomplete_crc'),
    url(r'cities-in-country.json$',
        cities_in_country, name='cities_in_country'),
)
