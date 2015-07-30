# -*- encoding: utf-8 -*-

""" 
After importing profiles, each profile only has a crc string made from the old
fixed values for "country" and "region" plus the old free text value for "city".

Look through all the UserProfile.crc fields and try to find accurate geo names 
from the "dtrcity" tables, and link the to the user profile, so that they have 
well-defined and valid geo info attached, i.e., "city", "region", "country", 
"crc", "lat", "lng".

"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from dtrprofile.models import UserProfile
from dtrcity.models import Country, Region, City, AltName

class Command(BaseCommand):

    def handle(self, *args, **options):

        def find_altname(up):
            print u'a) Trying direct match...',
            try:
                an = AltName.objects.filter(crc__iexact=up.crc)[0]
                print u'woah :D matched: [{}]'.format(an.geoname_id)
                return an
            except IndexError:
                print u'not found, trying less exact...',
            try:
                an = AltName.objects.filter(crc__icontains=up.crc)[0]
                print u'woah :D matched: [{}]'.format(an.geoname_id)
                return an
            except IndexError:
                print u'not found again :('
            
            if up.crc.count(',') > 2: print 'Warning: more than 2 commas found!'
            xcity, xregion, xcountry = [x.strip() for x in up.crc.split(',', 2)]

            if xcity.lower() == 'guadalajara': 
                xcountry = 'mexico'
            if xregion.lower() == 'distrito capital' and xcountry.lower() == 'venezuela':
                xcity = 'caracas'
            if xcity.lower() == 'brooklyn': 
                xregion = 'nueva york'
            if xcity.lower() == 'lima': 
                xcountry = 'peru'
            if xcity.lower() == 'puebla': 
                xregion = 'puebla'
                xcountry = 'mexico'

            print u'b) Trying city, region, country match: "{}" + "{}"...'.format(xcity, xregion, xcountry),
            if xcity in ('', 'None') or xregion in ('', 'None') or xcountry in ('', 'None'):
                print 'None value found, skip this test.'
            else:
                try:
                    an = AltName.objects.filter(crc__istartswith=xcity).filter(crc__icontains=xregion).filter(crc__iendswith=xcountry)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying less exact...',
                try:
                    an = AltName.objects.filter(crc__icontains=xcity).filter(crc__icontains=xregion).filter(crc__icontains=xcountry)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again :('

            print u'c) Trying city and region match: "{}" + "{}"...'.format(xcity, xregion),
            if xcity in ('', 'None') or xregion in ('', 'None'):
                print 'None value found, skip this test.'
            else:
                try:
                    an = AltName.objects.filter(crc__istartswith=xcity).filter(crc__iendswith=xregion)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying less exact...',
                try:
                    an = AltName.objects.filter(crc__icontains=xcity).filter(crc__icontains=xregion)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again :('

            print u'd) Trying city and country match: "{}" + "{}"...'.format(xcity, xcountry),
            if xcity in ('', 'None') or xcountry in ('', 'None'):
                print 'None value found, skip this test.'
            else:
                try:
                    an = AltName.objects.filter(crc__istartswith=xcity).filter(crc__iendswith=xcountry)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying less exact...',
                try:
                    an = AltName.objects.filter(crc__icontains=xcity).filter(crc__icontains=xcountry)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again :('

            print u'e) Trying region and country match: "{}" + "{}"...'.format(xregion, xcountry),
            if xregion in ('', 'None') or xcountry in ('', 'None'):
                print 'None value found, skip this test.'
            else:
                try:
                    an = AltName.objects.filter(crc__istartswith=xcountry).filter(crc__iendswith=xregion)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying less exact...',
                try:
                    an = AltName.objects.filter(crc__icontains=xcountry).filter(crc__icontains=xregion)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again :('

            print u'f) Trying match only by city name: "{}"...'.format(xcity),
            if xcity in ('', 'None'):
                print u'None value found, skip this test.'
            else:
                xcity_comma = u'{},'.format(xcity)
                try:
                    an = AltName.objects.filter(crc__istartswith=xcity_comma)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying less exact...',
                try:
                    an = AltName.objects.filter(crc__istartswith=xcity)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found, trying even less exact...',
                try:
                    an = AltName.objects.filter(crc__icontains=xcity_comma)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again, last try...'
                try:
                    an = AltName.objects.filter(crc__icontains=xcity)[0]
                    print u'woah :D matched: [{}]'.format(an.geoname_id)
                    return an
                except IndexError:
                    print u'not found again :('

            return None

        # ----------------------------------------------------------------------
        #
        # main
        #
        # ----------------------------------------------------------------------

        print u'UserProfiles available: {}'.format(UserProfile.objects.all().count())

        upfixed = i = found = notfound = 0

        for up in UserProfile.objects.all().order_by('pk'):
            i += 1
            print
            print u'{}. ----- [{}] from "{}" -----'.format(i, up.user_id, up.crc)

            #if up.city is not None:
            #    print u'User [{}] has a city defined. Skip.'
            #    continue;
            if not up.crc:
                print u'User [{}] has no crc value. Skip.'
                continue;

            xaltname = find_altname(up)
            if xaltname is None: 
                notfound += 1
                continue

            print u'"{}" -->'.format(xaltname.crc),

            try:
                altname = AltName.objects.get(geoname_id=xaltname.geoname_id, 
                                        language=settings.LANGUAGE, is_main=1)
            except:
                print u'argh! =:-O altname not found! Abort! Skip! Aaaargh!'
                notfound += 1
                continue

            print u'"{}"'.format(altname.crc)
            found += 1

            # Now add the geo data to the user's profile.
            print '#',
            country = Country.objects.get(pk=altname.country_id)
            print '#',
            region = Region.objects.get(pk=altname.region_id)
            print '#',
            city = City.objects.get(pk=altname.geoname_id)
            print '#',
            up.crc = altname.crc
            print '#',
            up.lat = altname.lat
            print '#',
            up.lng = altname.lng
            print '#',
            up.city = city
            print '#',
            up.region = region
            print '#',
            up.country = country
            print '#',
            up.altname = altname
            print '#',
            up.save()
            print '#',
            upfixed += 1
            print

        print
        print 'Result: [{}] items with [{}] locations found and [{}] locations unknown. Fixed [{}] userprofiles.'.format(i, found, notfound, upfixed)
        print


