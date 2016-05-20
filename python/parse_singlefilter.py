import json
from astropy.table import Table

path = '/Users/willettk/Astronomy/Research/GalaxyZoo/single_filter'

def parse_subjects():

    subfile = '%s/sloan_singleband_subjects.csv' % path
    with open(subfile,'r') as f:
        lines = f.readlines()
    
    # Initialize new Table

    t = Table()

    # Populate it with the first record

    j0 = json.loads(lines[0].strip())
    t['_id'] = ['ObjectId("%s")' % j0['_id']['$oid']]
    t['zooniverse_id'] = [j0['zooniverse_id']]
    t['image_id'] = [j0['metadata']['provided_image_id']]
    t['sdss_id'] = [j0['metadata']['sdss_id']]
    t['survey'] = [j0['metadata']['survey']]
    t['band'] = [j0['metadata']['band']]
    t['state'] = [j0['state']]
    t['classification_count'] = [j0['classification_count']]
    t['counters_feature'] = [j0['metadata']['counters']['feature']]
    t['counters_smooth'] = [j0['metadata']['counters']['smooth']]
    t['counters_star'] = [j0['metadata']['counters']['star']]
    t['ra'] = [j0['coords'][0]]
    t['dec'] = [j0['coords'][1]]
    t['petroR50_r'] = [j0['metadata']['petroflux_r']]
    t['petroR50_r_kpc'] = [j0['metadata']['absolute_size']]
    t['mag_u'] = [j0['metadata']['mag']['u']]
    t['mag_g'] = [j0['metadata']['mag']['g']]
    t['mag_r'] = [j0['metadata']['mag']['r']]
    t['mag_i'] = [j0['metadata']['mag']['i']]
    t['mag_z'] = [j0['metadata']['mag']['z']]
    t['absmag_r'] = [j0['metadata']['mag']['abs_r']]
    t['petroflux_r'] = [j0['metadata']['petroflux_r']]
    t['redshift'] = [j0['metadata']['redshift']]
    
    # Loop over file
    for line in lines[1:]:
        j = json.loads(line.strip())
        t.add_row((
            "ObjectId(%s)" % j['_id']['$oid'],
            j['zooniverse_id'],
            j['metadata']['provided_image_id'],
            j['metadata']['sdss_id'],
            j['metadata']['survey'],
            j['metadata']['band'],
            j['state'],
            j['classification_count'],
            j['metadata']['counters']['feature'],
            j['metadata']['counters']['smooth'],
            j['metadata']['counters']['star'],
            j['coords'][0],
            j['coords'][1],
            j['metadata']['petroflux_r'],
            j['metadata']['absolute_size'],
            j['metadata']['mag']['u'],
            j['metadata']['mag']['g'],
            j['metadata']['mag']['r'],
            j['metadata']['mag']['i'],
            j['metadata']['mag']['z'],
            j['metadata']['mag']['abs_r'],
            j['metadata']['petroflux_r'],
            j['metadata']['redshift']
            ))


    t.write('%s/sloan_singleband_subjects.fits' % path,format='fits')

    return None

def parse_classifications():

    classfile = '%s/classifications_10_Jun_2015.csv' % path
    with open(classfile,'r') as f:
        lines = f.readlines()
    
    # Initialize new Table

    t = Table()

    # Populate blank columns

    rownames = ['_id',
            'subject_id',
            'zooniverse_id'] + ['sloan_singleband-%i'%i for i in range(12)]
    rowdtype = ['S38','S38','S10']+['S4']*12
    rowdtype[9] = 'S24'
    t = Table(
        names=tuple(rownames),
        dtype=tuple(rowdtype))

    # Loop over file

    for line in lines:
        j = json.loads(line.strip())

        annrow = ['']*12
        for i in range(12):
            for a in j['annotations']:
                if 'sloan_singleband-%i' % i in a:
                    annrow[i] = a['sloan_singleband-%i' % i]

        # Check specifically for sloan_singleband-6 (odd features)
        # Can be either a single answer "a-0", or a list of odd features ["a-0","x-1","x-3"]

        if annrow[6] != None:
            if type(annrow[6]) == list:
                annrow[6] = ','.join(annrow[6][1:])

        row = ['ObjectId("%s")' % j['_id']['$oid'],
            'ObjectId("%s")' % j['subjects'][0]['id']['$oid'],
            j['subjects'][0]['zooniverse_id']] + annrow
        t.add_row(tuple(row))

    t.write('%s/classifications_10_Jun_2015.fits' % path,format='fits')

    return None
