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
		$("#upload").attr('href','javascript:upload_dialog("",function() {}, function(){})');
	} else {
		$("#upload").attr('href',window.location.origin + "/Tracks/signin/");
	}
}

function uploadFile() {
	$("#uploadNav").submit();
}

	/** ADD A DESCRIPTION */
	function upload_dialog(dialog_text, yes_funcToExecute, no_funcToExecute) {
		var dialog_box = $("<div id='upload_dialog'></div>").appendTo("body").html("<ul><li><form id='navbar-upload' action='/' method='post'><input id='navbar_file' type='file' name='file'></input></form></li></ul>");
		$('#navbar_file').attr('onchange','file_load(this)');
		$(dialog_box).dialog({
			modal: true,
			height: 240,
			widgth: 360,
			resizable: false,
			draggable: false,
			title: "Upload Tracks",
			dialogClass: "confirm_dialog",
			open: function () {
				$(this).siblings('.ui-dialog-buttonpane').find('button:eq(1)').focus();
			},
			buttons: {
				"Finish": function () {
					yes_funcToExecute();
					$(this).dialog("close");
				}
			},
			close: function (event, ui) {
				$(this).remove();
			}
		});
		$("#navbar-upload").attr("action","/Tracks/upload_mp3");

	}

	/** ADD A DESCRIPTION */
	function navbar_create_music_player(audio_name) {
		var audio_div = $("<div></div>").addClass("audio_div").attr("name", audio_name);
		// To be changed later (media_url)
		var media_url = "http://127.0.0.1:8000/Tracks/user_mp3_files/";
		var temp_pathname = media_url + audio_name;
		var audio_control = $("<audio></audio>").attr("controls", "");
		var source = $("<source></source>").attr("type", "audio/mpeg").attr("src", temp_pathname);
		audio_control.append(source);
		audio_div.append(audio_control);
		return audio_div;
	}

	/** ADD A DESCRIPTION */
	function navbar_remove_music_player(music_player) {
		$(music_player).remove();
	}

	/** ADD A DESCRIPTION */
	function navbar_does_music_player_exist(html_element) {
		var music_player = $(html_element).siblings(".audio_div");
		if (music_player.length != 0) {
			return 1;
		} else {
			return 0;
		}
	}

	/** ADD A DESCRIPTION */
	function navbar_get_music_player(html_element) {
		var music_player;
		if (navbar_does_music_player_exist(html_element)) {
			music_player = $(html_element).siblings(".audio_div").get(0);
			return music_player;
		} else {
			var parent = $(html_element).parent();
			music_player = navbar_create_music_player(html_element.name);
			$(music_player).hide();
			parent.append(music_player);
			return music_player;
		}
	}

	/** ADD A DESCRIPTION */
	function navbar_play_music(music_player) {
		var audio_control = $(music_player).children("audio").get(0);
		if (audio_control) {
			audio_control.play();
		}
	}


	/** ADD A DESCRIPTION */
	function navbar_pause_music(music_player) {
		var audio_control = $(music_player).children("audio").get(0);
		if (audio_control) {
			audio_control.pause();
		}
	}

	/** ADD A DESCRIPTION */
	function navbar_restart_music(music_player) {
		var audio_control = $(music_player).children("audio").get(0);
		if (audio_control) {
			audio_control.currentTime = 0;
		}
	}

	/**
	 * FUNCTIONALITY: Creates a new progress bar element.
	 * INPUTS: 1) html_element: The html element to add the progress bar to.
	 * OUTPUT: new_bar: The progress bar element.
	 */
	function navbar_add_new_progress_bar(html_element) {
		var new_bar = $("<div></div>").addClass("progress_bar_container");

		$(html_element).children().last().after(new_bar);

		$(html_element).children(".progress_bar_container").append(
		$("<div></div>").addClass("progress_bar_outer"));

		$(html_element).children(".progress_bar_container").append(
		$("<div></div>").addClass("progress_bar_inner"));

		return new_bar;
	}

	/**
	 * FUNCTIONALITY: Creates a "track element" - i.e. an li element with text and a progress bar.
	 * The "track element" represents a file which is in the process of uploading.
	 * INPUTS: 1) preceding_text: The text to add before the progress bar.
	 *         2) element_to_add_before_to: The html element which the "track element"
	 *            will be added before to (preferably the <li> container of an upload file form element).
	 * OUTPUT: new_bar: The progress bar element of the "track element".
	 */
	function navbar_add_loading_track(preceding_text, element_to_add_before_to) {
		var temp = $("<li></li>").append(
		$("<span></span>").text(preceding_text + " "));
		var new_bar = navbar_add_new_progress_bar(temp);
		$(element_to_add_before_to).before(temp);
		return new_bar;
	}

	/**
	FUNCTIONALITY: Sets the length of the inner filling of the progress bar to visually indicate how much progress has been made.
	 * INPUTS: 1) progress_bar: The progress bar to set the filling of.
	 *         2) percent_0_to_100: The percent (range 0 to 100) of the progress bar that should be filled.
	 * OUTPUT: None
	 */
	function navbar_progress_bar_setPercent(progress_bar, percent_0_to_100) {
		var progress_bar_max_width = parseInt($(progress_bar).children("div.progress_bar_outer").css("width"), 10);
		//alert(progress_bar_max_width);
		var inner = $(progress_bar).children("div.progress_bar_inner");
		var margin = $(inner).css("margin-top");
		var progress_bar_inner_margin_offset = parseInt(margin, 10);
		var progress_bar_width = percent_0_to_100 * (progress_bar_max_width / 100) - 2 * progress_bar_inner_margin_offset;
		progress_bar_width = progress_bar_width.toString() + "px";
		//alert(progress_bar_width);
		$(progress_bar).children("div.progress_bar_inner").css("width", progress_bar_width);

		if (percent_0_to_100 == 100) {
			$(progress_bar).children("div.progress_bar_inner").css("background-color", "#41DD00");
		}
	}

	/** FUNCTIONALITY: Sets the inner filling of the progress bar to red in order to visually indicate a failure.
	 * INPUTS: 1) progress_bar: The progress bar to set the filling of.
	 * OUTPUT: None
	 */
	function navbar_progress_bar_Failure(progress_bar) {
		$(progress_bar).children("div.progress_bar_inner").css("background-color", "red");
	}

	/** FUNCTIONALITY: An event handler used for the event of a file upload in progress. Updates the progress bar appropriately.
	 * INPUTS: 1) evt: The event object.
	 *         2) progress_bar: The progress bar to set the filling of.
	 * OUTPUT: None
	 */
	function navbar_progressHandler(evt, progress_bar) {
		if (evt.lengthComputable) {
			var percent_done = parseInt(100.0 * evt.loaded / evt.total);
			navbar_progress_bar_setPercent(progress_bar, percent_done);
		}
	}

	/** FUNCTIONALITY: An event handler used for the event of a file upload which failed. Updates the progress bar appropriately.
	* INPUTS: 1) evt: The event object.
	*         2) progress_bar: The progress bar to set the filling of.
	* OUTPUT: None
	*/
	function uploadFailedHandler(evt, progress_bar) {
		progress_bar_Failure(progress_bar);
	}

	/** FUNCTIONALITY: Handles uploading a file to the server asynchronously.
	 * This includes:
	 *    - sending data to the server (and waiting for the response).
	 *    - updating the UI to reflect the progress of the file upload.
	 * INPUTS: None
	 * OUTPUT: None
	 */

	function file_load(elem) {
		// gets the file from the file input and prepares it for uploading
		var form_data = new FormData();
		if (!$(elem).val()) {
			return
		}
		var file_input = $(elem)[0];
		var file = file_input.files[0];
		form_data.append('file', file);
		//form_data.append('user_email', '{{ user.email }}');

		// updates the UI to reflect a file which is uploading
		var new_bar = navbar_add_loading_track(file.name, $(elem).parents(".tracks_list_authorized_buttons_item"));

		// updates the UI to allow the user to upload another file while the previous file is uploading
		$(elem).parents("form").get(0).reset();

		// the ajax request to the server to upload the file
		$.ajax({
			url: window.location.origin+"/Tracks/upload_mp3/",
			type: 'POST',
			data: form_data,
			cache: false,        // tell the browser not to use its cache
			processData: false,  // we already have a FormData obj, so $ needs to leave it alone
			contentType: false,  // $ needs to leave the contentType alone
			xhr: function () {
				var xhr = jQuery.ajaxSettings.xhr();
				if (xhr.upload) {
					xhr.upload.addEventListener('progress', function (evt) { navbar_progressHandler(evt, new_bar) }, false);
					xhr.upload.addEventListener("error", function (evt) { navbar_uploadFailedHandler(evt, new_bar) }, false);
				}//if
				return xhr;
			},
			success: function (data, textStatus, jqXHR) {
				//alert(jqXHR.responseText);
				server_filename = data["server_filename"];
				track_id = data["track_id"];
				var height = $("#upload_dialog").attr('height') + 50;
				$("#upload_dialog").attr('height',height);
				navbar_update_completed_loading_track(new_bar, server_filename, track_id);

			},
			error: function (jqXHR, textStatus, errorThrown) {
				navbar_progress_bar_Failure(new_bar);
				console.log(jqXHR.responseText);
			},
			async: true

		});
	}

	/** ADD A DESCRIPTION */
	function navbar_update_completed_loading_track(progress_bar, server_filename, track_id){
		var show_player_button = navbar_create_show_player_button(server_filename);
		$(progress_bar).before(show_player_button);
		$(progress_bar).after(" ");
		$(progress_bar).remove();
	}

	/** ADD A DESCRIPTION */
	function navbar_create_show_player_button(server_filename){
		var show_player_button = $("<button></button>").attr("name", server_filename);
		$(show_player_button).addClass("show_hide_player_button");
		$(show_player_button).text("Show Player");
		$(show_player_button).bind("click", navbar_show_player);
		return show_player_button;
	}

        function navbar_show_player() {
            var music_player = navbar_get_music_player(this);
             navbar_play_music(music_player);
            $(music_player).show(500);
            $(this).unbind("click");
            $(this).bind("click", navbar_hide_player);
            $(this).text("Hide Player");
        }

        /** ADD A DESCRIPTION */
        function navbar_hide_player() {
            if (does_music_player_exist(this)) {
                var music_player = navbar_get_music_player(this);
                //pause_music(music_player);
                //$(music_player).hide(500);
                $(music_player).hide(500, function () {
                pause_music(music_player);
                });
                //$(music_player).hide(500, function (){ remove_music_player(music_player);});

                $(this).unbind("click");
                $(this).bind("click", show_player);
                $(this).text("Show Player");
            }
        }

        /********************** The following methods are not mine, they are from Django. *****************************
        ******* They allow safe POSTing with Jquery/AJAX (e.g. proper CSRF token, proper origin of request, etc.) *******/
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        function sameOrigin(url) {
            // test that a given url is a same-origin URL
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    var csrftoken = $('input[name=csrfmiddlewaretoken]').val();
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

