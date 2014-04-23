/** Check if user is logged on. */
function addNav(session) {
    $("#navbar").html('<div class="container">'
                    +     '<div class="navbar-header">'
                    +       '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">'
                    +         '<span class="sr-only">Toggle navigation</span>'
                    +         '<span class="icon-bar"></span>'
                    +         '<span class="icon-bar"></span>'
                    +         '<span class="icon-bar"></span>'
                    +       '</button>'
                    +         '<a id="tracks_home" class="navbar-brand" href="">Tracks</a>'
                    +     '</div>'
                    +     '<div class="collapse navbar-collapse">'
                    +       '<ul id="navbar_options" class="nav navbar-nav"> </ul>'
                    +       '<form method="GET" class="navbar-form" role="search">'
                    +         '<div class="form-group">'
                    +           '<input type="text" name="search" class="form-control" placeholder="search">'
                    +         '</div>'
                    +         '<button type="submit" class="btn btn-default">'
                    +           '<span class="glyphicon glyphicon-music"></span>'
                    +         '</button>'
                    +       '</form>'
                    +     '</div>'
                    +     '<!--/.nav-collapse -->'
                    +   '</div>')
    // $("#navbar").html('<div class="container"><div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><a id="tracks_home" class="navbar-brand" href="">Tracks</a></div><div class="collapse navbar-collapse"><ul id="navbar_options" class="nav navbar-nav"> </ul><form method="GET" class="navbar-form" role="search"><div class="form-group"><input type="text" name="search" class="form-control" placeholder="search"></div><button type="submit" class="btn btn-default"><span class="glyphicon glyphicon-music"></span></button></form></div><!--/.nav-collapse --></div>')

    if (session) {
        $("#navbar_options").html('<li><a id="downbeat">Downbeat</a></li>'
								+ '<li><a id="profile">Profile</a></li>'
								+ '<li><a id="collab">Collaborations</a></li>'
                                + '<li><a type="file" id="upload">Upload</a></li>'
                                + '<li><a id="about">About</a></li>'
                                + '<li> <a id="signout">Sign out</a></li>')

    //if (true) {
        //$("#navbar_options").html('<li><a id="downbeat">Downbeat</a></li><li><a id="about">About</a></li><li><a id="upload">Upload</a></li><li> <a id="signout" href="javascript:signOut()">Sign out</a></li>')
    } else {
        // Show sign in link instead of projects, downbeat, profile, etc.
        $("#navbar_options").html('<li><a id="downbeat">Downbeat</a></li>'
								+ '<li><a id="profile">Profile</a></li>'
								+ '<li><a id="collab">Collaborations</a></li>'
                                + '<li><a id="upload">Upload</a></li>'
                                + '<li><a id="about">About</a></li>'
								+ '<li><a id="signin">Sign In/Register</a></li>')
    }
    hrefCreate(session);
	$("body").append('<style>'
	+'.ui-dialog'
       + '{'
       + 'border: none;'
       + 'padding: 0px 0px 0px 0px;'
       + 'border-radius: 0px;'
       + 'box-shadow: 0px 0px 10px 2px #888888;'
    +    '}'
    +    '.confirm_dialog .ui-dialog-titlebar'
    +    '{'
    +        'border: 1px solid black;'
    +        'background: none;'
    +        'background-color: black;'
    +        'border-radius: 0px;'
    +        'color: white;'
    +        'padding: 2px 2px 2px 10px;'
    +    '}'
    +    '.confirm_dialog .ui-dialog-titlebar-close'
    +    '{'
    +        'display: none;'
    +  '}'
    +   '.confirm_dialog .ui-dialog-content'
    +    '{'
    +    '}'
    +    '.confirm_dialog .ui-dialog-buttonpane'
    +    '{'
    +        'padding: 0 0 0 0;'
    +    '}'
    +    '.confirm_dialog .ui-dialog-buttonset button'
    +    '{'
    +       'border: 1px solid black;'
    +        'background: none;'
    +        'background-color: black;'
    +        'margin: 1px 1px 1px 1px;'
    +        'width: 60px;'
    +        'color: white;'
    +        'border-radius: 0px;'
    +    '}'
    +    '.confirm_dialog .ui-dialog-buttonset .ui-button-text'
    +   '{'
    +       'padding: 1px 1px 1px 1px;'
    +    '}'
    + '</style>'
	)
}

/** ADD A DESCRIPTION */
function hrefCreate(session) {
    if (!window.location.origin) {
      window.location.origin = window.location.protocol + "//" + window.location.hostname + (window.location.port ? ':' + window.location.port: '');
    }
    $("#tracks_home").attr('href',window.location.origin+"/Tracks");
    $("#downbeat").attr('href', window.location.origin+"/Tracks/downbeat/");
    $("#about").attr('href', window.location.origin+"/Tracks/about.html");
    $("#collab").attr('href', window.location.origin+"/Tracks/userpage/");
    $("#signout").attr('href', window.location.origin+"/Tracks/logout/");
	$("#profile").attr('href', window.location.origin+"/Tracks/userprofile/");
	$("#signin").attr('href', window.location.origin+"/Tracks/signin/");
    $(".navbar-form").attr('action', window.location.origin+"/Tracks/search/");
	if(session){
		//$("#upload").attr('href','javascript:upload_dialog("",function() {}, function(){})');
        $("#upload").attr('href', "javascript:;");
        $("#upload").on("click", upload_dialog);
	} else {
		$("#upload").attr('href',window.location.origin + "/Tracks/signin/");
	}
}

/*
function uploadFile() {
	$("#uploadNav").submit();
}
*/

function upload_dialog(){
    var dialog_html = $("<table></table>").addClass("tracks_list").append(create_tracks_authorized_buttons_html());
    var title = "Add New Track";
    var width = 640;
    var height = 250;

    $(dialog_html).find('.musicUpload input[name="file"]').on("change", upload_file);

    var action_func_kv_obj = { "Finish" : function(){
                                     $(dialog_html).find('.musicUpload input[name="file"]').off("change", upload_file);
                                     }
                                };

    dialog_box(dialog_html, title, width, height, action_func_kv_obj);
}


