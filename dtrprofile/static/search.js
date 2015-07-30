
login_required();

$(document).ready(function(){
    fix_search_options();
    render_selected_search();
    render_search_results('#results', {'minage': localStorage.search_minage, 
                                       'maxage': localStorage.search_maxage, 
                                       'gender': localStorage.search_gender, 
                                       'city': localStorage.search_city,
                                       'dist': localStorage.search_dist, 
                                       'count': 100 });

    // Load countries and current cities.
    console.log('Loading all countries...');
    $.get('/api/v1/all-countries.json', {}, function(data){
        var html = '';
        data.forEach(function(row, i){
            var sel = (row[0] == localStorage.search_country ? ' selected' : '');
            html += '<option value="' + row[0] + '"' + sel + '>' + row[1] + '</option>';
        });
        $('#search-form select[name="country"]').html(html);

        fill_city_options_for_country(localStorage.search_country);
    });

    // Display city select form when city name was clicked.
    $('#search-form').on('click', '.city', function(e){
        $('#search-form .city-opts').css({"display":"block"});
    });

    // Load new cities list when a new country was selected.
    $('#search-form select[name="country"]').on('change', function(e){
        var country = $(this).val();
        fill_city_options_for_country(country);
    });

    // When search form is submitted, fix up search vals, get a matching user
    // list from server, and render it.
    $('#search-form').on('submit', function(e){
        e.preventDefault(); e.stopPropagation();

        // Store selected options locally.
        localStorage.search_gender = $('#search-form select[name="gender"]').val();
        localStorage.search_minage = $('#search-form input[name="minage"]').val();
        localStorage.search_maxage = $('#search-form input[name="maxage"]').val();

        // Only update search vals for country/city if there is actually anything selected:
        if ( $('#search-form select[name="city"] option:selected').length > 0 ){
            localStorage.search_country = $('#search-form select[name="country"]').val();
            localStorage.search_city = $('#search-form select[name="city"]').val();
            localStorage.search_dist = $('#search-form select[name="dist"]').val();
            localStorage.search_crc = $('#search-form select[name="city"] option:selected').text();
            $('#search-form .city').html(localStorage.search_crc);
            $('#search-form .city-opts').hide();
        };

        // Send GET to the search API, it'll use the cookie to get results.
        render_search_results('#results', {'minage': localStorage.search_minage, 
                                           'maxage': localStorage.search_maxage, 
                                           'gender': localStorage.search_gender, 
                                           'city': localStorage.search_city,
                                           'dist': localStorage.search_dist, 
                                           'count': 100 });
    });
});

//////
// Uses the currently set localStorage.search_country value and loads all 
// related cities. Sets localStorage.search_city as default city, if its in
// the cities list.
function fill_city_options_for_country(country){
    console.log('Loading cities for country...'); 
    console.log(country);
    if (!country) { console.log('Uh! No country.'); return ''; }
    var params = { 'q':country };
    console.log(params);
    $('#search-form select[name="city"]').html('<option value="">Loading...</option>');

    $.get('/dtrcity/cities-in-country.json', params, function(data){
        var html = '';
        data.forEach(function(row, i){
            var sel = (row[0] == localStorage.search_city ? ' selected' : '');
            html += '<option value="' + row[0] + '"' + sel + '>' + row[1] + '</option>';
        });
        $('#search-form select[name="city"]').html(html);
    });
}

//////
// Make sure all search options have a value set, or use default values.
function fix_search_options(){
    if ( typeof(localStorage.search_city) === 'undefined' 
      || localStorage.search_city == null 
      || localStorage.search_city == "null" 
      || localStorage.search_city == ''
      || !localStorage.search_city
      || typeof(localStorage.search_country) === 'undefined' 
      || localStorage.search_country == null 
      || localStorage.search_country == "null" 
      || localStorage.search_country == ''
      || !localStorage.search_country
      || typeof(localStorage.search_crc) === 'undefined' 
      || localStorage.search_crc == null 
      || localStorage.search_crc == "null"
      || localStorage.search_crc == ''
      || !localStorage.search_crc ){

        localStorage.search_country = window.authuser.country;
        localStorage.search_city = window.authuser.city;
        localStorage.search_crc = window.authuser.crc;
    }

    if ( typeof(localStorage.search_dist) === 'undefined' 
      || localStorage.search_dist == null 
      || localStorage.search_dist == "null" 
      || localStorage.search_dist == ''
      || !localStorage.search_dist ) localStorage.search_dist = 5;

    if ( localStorage.search_minage == '' ) localStorage.search_minage = 18;
    if ( localStorage.search_maxage == '' ) localStorage.search_maxage = 99;
    if ( parseInt(localStorage.search_minage) < 18 ) localStorage.search_minage = 18;
    if ( parseInt(localStorage.search_minage) > 80 ) localStorage.search_minage = 80;
    if ( parseInt(localStorage.search_maxage) > 99 ) localStorage.search_maxage = 99;
    if ( parseInt(localStorage.search_minage) > parseInt(localStorage.search_maxage) ) 
        localStorage.search_maxage = parseInt(localStorage.search_minage) + 1;

    if (typeof(window.gender_names[localStorage.search_gender]) === 'undefined') 
        localStorage.search_gender = get_default_search_gender();
}

function get_default_search_gender(){
    if (window.authuser.gender ===   '1') return 8; // Straight men (1) --> straight women (8)
    if (window.authuser.gender ===   '2') return 2; // Gay men (2) --> gay men (2)
    if (window.authuser.gender ===   '4') return 64; // etc.
    if (window.authuser.gender ===   '8') return 1;
    if (window.authuser.gender ===  '16') return 16;
    if (window.authuser.gender ===  '32') return 128;
    if (window.authuser.gender ===  '64') return 4;
    if (window.authuser.gender === '128') return 32;
    if (window.authuser.gender === '256') return 256;
}

function render_selected_search(){
    $('#search-form .options-box').remove();

    // Make sure all search options are valid.
    fix_search_options();

    // gender options
    var html = '';
    $.each(window.gender_plurals, function(k, v){ html += '<option value="' + k + '"' + (localStorage.search_gender == k ? ' selected':'') + '> ' + v + '</option>'; });
    $('#search-form select[name="gender"]').append(html);

    // Set initial values in search row.
    $('#search-form input[name="minage"]').val(localStorage.search_minage);
    $('#search-form input[name="maxage"]').val(localStorage.search_maxage);
    $('#search-form .city').html(localStorage.search_crc);

}
