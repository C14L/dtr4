from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseNotFound            # 404
from django.http import HttpResponsePermanentRedirect   # 301
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.views.decorators.cache import cache_page

from dtrcity.models import Region, City, AltName
from dtrprofile.models import UserProfile

"""
This app mainly provides landing pages for all dater3 areas, and makes sure
that well-indexed pages from the EL Ligue PHP version remain indexed under the
original URL, or are properly redirected.
"""


# noinspection PyUnusedLocal
def redir_to_status_stream(req):
    return HttpResponsePermanentRedirect('/u/')


# noinspection PyUnusedLocal
def redir_old_user_pages(req, username):
    user = get_object_or_404(User, username=username)
    url = reverse('user_profile', kwargs={'username': user.username})
    return HttpResponsePermanentRedirect(url)


# noinspection PyUnusedLocal,PyUnresolvedReferences
def redir_old_forum_threads(req, threadid):
    # TODO: Doesn't work yet.
    """
    OLD: /thread/describe-al-de-arriba-17452-1420.html
    NEW: /f/Erotico/c2X3-1/que-les-gusta-a-las-mujeres-en-un-hombre-fisicamente/
    """
    # Find thread ID translation.
    ot = get_object_or_404(OldThread, old_threadid=threadid)
    # Fetch new thread starter Post.
    nt = get_object_or_404(Post, pk=ot.pk)
    url = reverse('dtrforum_read_thread', kwargs={
                  'boardname': nt.board.name, 'slug': utils.slugify(nt.title),
                  'thread_encid': utils.num_encode(nt.id), 'page': 1, })
    return HttpResponsePermanentRedirect(url)


@cache_page(60 * 60 * 24 * 365)
def users_alphabetically(req):  # URL path: /browse.php?begin=ab
    ctx = {'letter': req.GET.get('begin', '').lower()}

    if len(ctx['letter']) < 2:
        tpl = 'dtrseo/list_of_letters.html'
    else:
        tpl = 'dtrseo/list_of_users_by_letter.html'

        ctx['userprofiles'] = UserProfile.objects.filter(
            user__username__istartswith=ctx['letter'],
            user__is_active=True,
            pic__isnull=False
        ).order_by('user__username').prefetch_related('user', 'city')[:100]

    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def users_f_m(req, tpl='dtrseo/list_of_users_f_m.html'):  # 20==woman
    ctx = {
        'userprofiles': UserProfile.objects.filter(
            gender__in=(4, 5),
            user__is_active=True,
            pic__isnull=False
        ).order_by('-user__last_login').prefetch_related('user')[:100]
    }
    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def users_m_f(req, tpl='dtrseo/list_of_users_m_f.html'):
    ctx = {
        'userprofiles': UserProfile.objects.filter(
            gender__in=(1, 2),
            user__is_active=True,
            pic__isnull=False
        ).order_by('-user__last_login').prefetch_related('user')[:100]
    }
    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def users_f_pics(req, tpl='dtrseo/list_of_users_f_pics.html'):
    ctx = {
        'userprofiles': UserProfile.objects.filter(
            gender__in=(4, 5),
            user__is_active=True,
            pic__isnull=False
        ).order_by('-user__last_login').prefetch_related('user')[:100]
    }
    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def users_m_pics(req, tpl='dtrseo/list_of_users_m_pics.html'):
    ctx = {
        'userprofiles': UserProfile.objects.filter(
            gender__in=(1, 2),
            user__is_active=True,
            pic__isnull=False
        ).order_by('-user__last_login').prefetch_related('user')[:100]
    }
    return render(req, tpl, ctx)


# noinspection PyUnusedLocal
@cache_page(60 * 60 * 24 * 365)
def citymx(req, city_short, city_name, tpl='dtrseo/es_citymx.html'):
    # The old URLs to some Mexican cities, e.g. "/citymxmer/merida.html‎"
    abbr_cities = {
        'aca': 3533462,  # 'Acapulco',
        'cam': 3531732,  # 'Campeche',
        'can': 3531673,  # 'Cancún',
        'chi': 4014338,  # 'Chihuahua',
        'jua': 4013708,  # 'Ciudad Juárez',
        'cue': 3529947,  # 'Cuernavaca',
        'gua': 4005539,  # 'Guadalajara',
        'her': 4004898,  # 'Hermosillo',
        'leo': 3998655,  # 'León',
        'maz': 3996322,  # 'Mazatlán',
        'mer': 3523349,  # 'Mérida',
        'mex': 3996069,  # 'Mexicali',
        'mdf': 3530597,  # 'Mexico D.F.',
        'mty': 3995465,  # 'Monterrey',
        'nog': 4004886,  # 'Nogales',
        'lar': 3522551,  # 'Nuevo Laredo',
        'oax': 3522507,  # 'Oaxaca',
        'pac': 3522210,  # 'Pachuca',
        'pue': 3521081,  # 'Puebla',
        'qro': 3991164,  # 'Querétaro',
        'slp': 3985606,  # 'San Luís Potosí',
        'tam': 3516355,  # 'Tampico',
        'tap': 3516266,  # 'Tapachula',
        'tij': 3981609,  # 'Tijuana',
        'tol': 3515302,  # 'Toluca',
        'tor': 3981254,  # 'Torreón',
        'tux': 3515001,  # 'Tuxtla Gutiérrez',
        'ver': 3514783,  # 'Veracruz',
        'vil': 3514670,  # 'Villahermosa',
        'xal': 3526617,  # 'Xalapa',
        'zac': 3979844,  # 'Zacatecas',
        # 'aaa': 'Otra ciudad mexicana',
        # 'bbb': 'Fuera de México',
    }

    # Find the city id by place name.
    if city_short not in abbr_cities.keys():
        return HttpResponseNotFound()
    city = City.objects.get(pk=abbr_cities[city_short])
    cities = City.get_cities_around_city(city)
    ctx = {
        'userprofiles': UserProfile.objects.filter(
            gender__in=[1, 2, 4, 5],
            city__in=cities,
            user__is_active=True,
            pic__isnull=False
        ).order_by('-user__last_login').prefetch_related('user', 'city')[:48],

        'city': get_object_or_404(
            AltName,
            geoname_id=abbr_cities[city_short],
            is_main=1,
            type=3,
            language=(get_language() or settings.LANGUAGE_CODE)[:2]
        ),
    }
    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def country_list(req, tpl='dtrseo/list_of_country.html'):
    """Show a list of some countries."""
    lim = [
        'Alemania', 'Antigua y Barbuda', 'Argentina', 'Armenia', 'Aruba',
        'Australia', 'Austria', 'Bahamas', 'Barbados', 'Bélgica', 'Belice',
        'Bermudas', 'Bolivia', 'Brasil', 'Canadá', 'Chile', 'Colombia',
        'Corea del Sur', 'Costa Rica', 'Cuba', 'Curazao', 'Dinamarca',
        'Dominica', 'Ecuador', 'El Salvador', 'España', 'Estados Unidos',
        'Filipinas', 'Francia', 'Granada', 'Guatemala', 'Guayana Francesa',
        'Guyana', 'Haití', 'Holanda', 'Honduras', 'Irlanda', 'Islandia',
        'Italia', 'Jamaica', 'México', 'Nicaragua', 'Noruega', 'Nueva Zelanda',
        'Panamá', 'Paraguay', 'Perú', 'Polonia', 'Portugal', 'Puerto Rico',
        'Reino Unido', 'República Dominicana', 'San Cristóbal y Nieves',
        'San Martín', 'San Vicente y las Granadinas', 'Santa Lucía', 'Suiza',
        'Trinidad y Tobago', 'Uruguay', 'Venezuela']
    ca = AltName.objects.filter(name__in=lim, type=1,
                                language=(get_language() or
                                          settings.LANGUAGE_CODE)[:2],
                                is_main=True).order_by('name')
    return render(req, tpl, {'country_altnames': ca})


@cache_page(60 * 60 * 24 * 365)
def users_by_country(req, country, tpl='dtrseo/list_of_users_by_country.html'):
    """Show list of regions of one country with some user profiles."""
    country_altname = get_object_or_404(
        AltName,
        slug=country,
        is_main=True,
        type=1,
        language=(get_language() or settings.LANGUAGE_CODE)[:2]
    )
    region_ids = [x.id for x in Region.objects.filter(
        country__pk=country_altname.geoname_id)]
    regions = AltName.objects.filter(
        type=2,
        language=(get_language() or settings.LANGUAGE_CODE)[:2],
        is_main=True,
        geoname_id__in=region_ids
    ).order_by('name')[:100]

    ctx = {'country': country_altname, 'region_altnames': regions}
    return render(req, tpl, ctx)


def users_by_country_region(req, country, region,
                            tpl='dtrseo/list_of_users_by_region.html'):
    """Show list of cities from a region/country with some profiles."""
    country_altname = get_object_or_404(
        AltName,
        slug=country,
        is_main=True,
        type=1,
        language=(get_language() or settings.LANGUAGE_CODE)[:2]
    )
    region_ids = [x.id for x in Region.objects.filter(
        country__pk=country_altname.geoname_id)]  # All regions of the country.

    try:
        # This should be able to use get_object_or_404() but there is data
        # inconsistency in the AltName table when countries have two regions
        # by the same name. Found the case of Lima, Peru that exists twice in
        # the regions table (ids: 3936451, 3936452), with different official
        # regions codes (PE.LMA, PE.15) and different cities/subdivisions below
        # it. Because 3936451 is the one for "peru/lima/lima" we just go with
        # that one for now, all imported users are below that geoname anyway,
        # TODO 2014-05-07 clean up the AltName table and rename those regions
        # so that region names and slugs with "is_main" status are always
        # unique. Seriously, why would a country have two regions with the same
        # name, anyways?!
        region_altname = AltName.objects.filter(
            slug=region,
            type=2,
            is_main=True,
            geoname_id__in=region_ids,
            language=(get_language() or settings.LANGUAGE_CODE)[:2]
        )[0]

    except IndexError:
        raise Http404()

    # region_altname = get_object_or_404(AltName, slug=region, type=2,
    #                                language=get_language(), is_main=True,
    #                                geoname_id__in=region_ids)
    region_altnames = AltName.objects.filter(
        type=2,
        language=(get_language() or settings.LANGUAGE_CODE)[:2],
        is_main=True,
        geoname_id__in=region_ids
    ).order_by('name')[:100]

    city_ids = [x.id for x in City.objects.filter(  # Other cities of region.
        region__pk=region_altname.geoname_id
    ).order_by('-population')[:50]]

    city_altnames = AltName.objects.filter(
        type=3,
        language=(get_language() or settings.LANGUAGE_CODE)[:2],
        is_main=True,
        geoname_id__in=city_ids
    ).order_by('name')[:100]

    ctx = {
        # 'userprofiles': userprofiles,
        'country': country_altname,
        'region': region_altname,
        'regions': region_altnames,
        'cities': city_altnames,
    }
    return render(req, tpl, ctx)


@cache_page(60 * 60 * 24 * 365)
def users_by_altname_url(req, crc_url,
                         tpl='dtrseo/list_of_users_by_altname_url.html'):
    """Shows a list of userprofiles from a city by its AltName.url value."""
    try:
        altname = AltName.objects.filter(
            url=crc_url,
            type=3,
            is_main=True,
            language=(get_language() or settings.LANGUAGE_CODE)[:2]
        )[0]

    except IndexError:
        raise Http404

    userprofiles = UserProfile.objects.filter(
        city=altname.geoname_id
    ).order_by('-user__last_login').prefetch_related('user', 'city')[:50]

    ctx = {'userprofiles': userprofiles, 'city': altname}
    return render(req, tpl, ctx)


"""
def forum_archive(req, tpl="dtrseo/forum_archive.html"):
    per_page = 25
    del_id = Post.get_status_id('deleted')
    count = Post.objects.filter(thread__isnull=True).extra(
        where=['NOT status & %s'], params=[del_id]).count()
    recount = Post.objects.filter(thread__isnull=False).extra(
        where=['NOT status & %s'], params=[del_id]).count()
    return render(req, tpl, {
        'count': count,
        'recount': recount,
        #'pages': range(int(count/per_page)+1, 0, -1),
    })
"""
