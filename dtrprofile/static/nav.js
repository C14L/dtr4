/*

Some common Javascript functions.

*/

// --- Settings ----------------------------------------------------------------

window.CSRF_COOKIE_NAME = 'nocsrf';
window.MEDIA_URL = '/pics/';
window.STATIC_URL = '/static/';

// -----------------------------------------------------------------------------

function urlencode(str){
    return encodeURIComponent(str);
}

function urldecode(str){
    return decodeURIComponent( ( str+'' ).replace( /\+/g, '%20' ) );
}

function set_cookie(name, value, days){
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    // Replace any ";" in value with something else
    value = ('' + value).replace(/;/g, ',');
    document.cookie = urlencode(name) + "=" + urlencode(value) + expires + "; path=/";
}

function get_cookie(name){
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0)
            return urldecode(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function delete_cookie(name){
    setCookie(name, "", -1);
}

// If user is not logged in, redir to login page.
function login_required(){
    if ( !window.authuser ) window.location.href = "/?next=" + 
                            encodeURIComponent(window.location.pathname);
}

// Continue to count the age of posts after they are rendered.
function update_time_deltas(){
    console.log('Updating timestamps...');
    // Calc timestamp time delta to current time.
    var now = new Date().getTime() / 1000;
    $('.timestamp').each(function(i, obj){
        var dif = (now - $(obj).attr('data-timestamp'));
        var unit = 'seconds'
        if (dif > 59) { dif /= 60; unit = 'minutes';
          if (dif > 59) { dif /= 60; unit = 'hours';
            if (dif > 23) { dif /= 24; unit = 'days';
              if (dif > 29) { dif /= 30; unit = 'months';
                if (dif > 11) { dif /= 12; unit = 'years'; 
        } } } } }
        if (dif < 0) dif = 0;
        $(obj).html(Math.floor(dif) + ' ' + unit);
    });
}

//////////
// Loads new search results list from server and creates DOM elements with the
// data that link to user profiles.
//
// Used e.g. in "search.html" and "profile.html #profilelinks".
//
// sel The DOM selector where the resulting HTML is inserted.
// param The search parameters, eg. minage, maxage, gender, city, etc.
function render_search_results(sel, param){
    //$(sel).html('Loading...');
    render_search_placeholder(sel);
    var html = '', i = 0;
    $.get('/api/v1/search.json', param, function(data){
        if ( data.length > 0 ){
            data.forEach( function(row, i){ 
                if ( i++ < param['count'] ){
                    var gender_symbol = window.gender_symbols[row['gender']] || '';
                    var city_name = get_city_name_from_crc(row['crc']);
                    var pic = get_pic_url(row['pic'], 'medium');

                    html += '<div data-user-id="' + row['id'] + '" class="useritem item">' +
                            '<div class="last-active">online <span class="timestamp" data-timestamp="' + row['last_active'] + '"></span> ago</div>' +
                            '<a class="userpic" href="/u/' + row['username'] + '" style="background-image:url(' + pic + ')"></a>' +
                            '<a class="username" href="/u/' + row['username'] + '">' + row['username'] + '</a>' +
                            '<div class="asl"><span class="age">' + row['age'] + '</span> <span class="gender">' + gender_symbol + '</span> <span class="crc">' + city_name + '</span></div>' +
                            '</div>'; 
                }
            });
        } else {
            html = 'Crickets...'
        }
      $(sel).html(html);
  }).error(function(err){
      $(sel).html('ERROR: ' + err.status + ': ' + err.statusText);
  });
};

/////////
// Renders empty search result items, as placeholders.
function render_search_placeholder(sel){
    var html = '';
    for (var i=0; i<50; i++){
        html += '<div class="useritem item">' +
                '<div class="last-active">online <span class="timestamp">10 mins</span> ago</div>' +
                '<a class="userpic" href="#" style="text-align:center"><span class="loading-spinner"><span></span><span></span><span></span></span></a>' +
                '<a class="username" href="#">Loading...</a>' +
                '<div class="asl"><span class="age">99</span> <span class="gender">?</span> <span class="crc">Loading...</span></div>' +
                '</div>'; 
    };
    $(sel).html(html);
}

//////////
// Check with server if authuser has new (unread) messages or new matches/likes.
function check_indicators(){
    var param = {};
    $.get('/api/v1/check_indicators.json', param, function(data){
        if (data["unread_messages_count"] > 0){
            $('.nav-indicator.unread-messages')
                .html(data["unread_messages_count"])
                .removeClass('hidden');
        }
        if (data["new_likedyou_count"] > 0 || data["new_matches_count"] > 0){
            $('.nav-indicator.new-matches')
                .html(data["new_likedyou_count"] + '/' + data["new_matches_count"])
                .removeClass('hidden');
        }
    });
};

function get_pic_url(pic_id, size){
    // Return the URL path to a user uploaded picture.
    // Path is: MEDIA_URL/size/pic_id_subdir/pic_id.jpg

    var placeholder = '/static/placeholder.jpg';
    var pics_per_subdir = 10000;
    var sizes = ["small","medium","large"];
    var szdirs = ["s","m","x"];
    var i = sizes.indexOf(size)
    if (i<0 || !pic_id) return placeholder;
    var szdir = szdirs[i]

    var getUrl = function(n){
        var subdir = Math.floor(n / pics_per_subdir);
        return window.MEDIA_URL  + szdir + '/' + subdir + '/' + n + '.jpg';
    }

    if (typeof(pic_id) == 'object') {
        var urls = [];
        for (i = 0; i < pic_id.length; i++) urls[i] = getUrl(pic_id[i]);
    } else {
        urls = getUrl(pic_id);
    }

    return urls;
}

function get_profile_url(username){
    // Return the profile URL.
    return '/u/' + username + '/';
}

function get_city_name_from_crc(crc){
    if (crc == '') return '';
    return crc.split(', ')[0];
}

function get_country_name_from_crc(crc){
    if (crc == '') return '';
    return crc.split(', ')[-1];
}

function get_csrf_token(){
    return get_cookie(window.CSRF_COOKIE_NAME);
}
