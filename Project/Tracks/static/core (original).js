$(document).ready(function () {

  /********************************** Functions of NISHANT KUMAR ***************************************/

    $(".settings_button").click(open_settings);
    $("#settings_div").hide();
    var button_using_settings_div;

    /** Opens a pane for settings of a collaboration. */
    function open_settings() {
        var prev_collab_style = collab_get_style(this);
        collab_set_style_to(this, "editing");
        if (button_using_settings_div !== this){
            $(button_using_settings_div).trigger("click");
            button_using_settings_div = this;
        }
        $("#settings_div").show("drop");
        var collab_id = get_collab_id(this);
        var this_button = this;
        $.getJSON(resolve_to_url["get_collab_settings_JSON_url"], {collab_id : collab_id}, function (data) {
            var current_permission_level = data["permission_level"];
            var permission_options_data = data["permission_options"];
            var authorized_users_data = data["authorized_users"];
            var temp_select_input = turn_KV_data_into_select_input(permission_options_data, "collab_permission_level", current_permission_level);
            var permission_element = $("<div></div>").addClass("collab_permission_div").append($("<span></span>").text("Permission Level: ")).append(temp_select_input);
            $(temp_select_input).on("change", function(){ change_permission_of_collab(this_button, temp_select_input) });
            var authorized_users_table = create_authorized_users_table(authorized_users_data, this_button);
            $("#settings_form").append(permission_element);
            $("#settings_form").append(authorized_users_table);
            $("#settings_form").append( $("<button></button>").text("Done").on("click", function() { close_settings(prev_collab_style, this_button); }) );
        });
        $(this_button).off("click");
        $(this_button).on("click", function(){
            close_settings(prev_collab_style, this_button);
            });
    }

    function close_settings(prev_collab_style, settings_button) {
        collab_set_style_to(settings_button, prev_collab_style);
        $("#settings_form").empty();
        $("#settings_div").hide("drop");
        $(settings_button).off("click");
        $(settings_button).on("click", open_settings);
    }

    function change_permission_of_collab(html_element_inside_collab, select_element){ // finish this
        var selected_value = $(select_element).children(":selected").val();
        collab_set_style_to(html_element_inside_collab, "processing");
        var collab_id = get_collab_id(html_element_inside_collab);
        $.ajax({
            url: resolve_to_url["change_permission_of_collab_url"],
            type: 'POST',
            data: {collab_id : collab_id, bool_permission : selected_value},
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                collab_set_style_to(html_element_inside_collab, "editing"); // set upon success of ajax

            },
            error: function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.responseText);
            },
            async: true

        });
    }

    function create_authorized_users_table(KV_data, this_button) {
        var temp_table = $("<table></table>").addClass("authorized_users_table");
        var first_row = $("<tr></tr>");
        $(first_row).append( $("<th></th>").text("User") );
        $(first_row).append( $("<th></th>").text("Can Modify?") );
        $(temp_table).append(first_row);
        $.each(KV_data, function (key, val) {
            var user_id = key;
            var name_to_display = val;
            var temp_row = $("<tr></tr>").attr("name", user_id);
            var remove_button = $("<button></button>").addClass("remove_user_from_collab").attr("name", user_id).text("Remove");
            $(remove_button).on("click", function(){ remove_user_from_collab(user_id, this_button) });
            $(temp_row).append( $("<td></td>").text(name_to_display) );
            $(temp_row).append( $("<td></td>").append(remove_button) );
            $(temp_table).append(temp_row);
            });
        var last_row = $("<tr></tr>");
        var add_user_text_input = $("<input></input>").attr("type", "text");
        var add_user_to_collab_button = $("<button></button>").on("click", function(){ add_user_to_collab(add_user_text_input, this_button) }).text("Add User"); // fix this
        $(last_row).append( $("<td></td>").append(add_user_text_input) );
        $(last_row).append( $("<td></td>").append(add_user_to_collab_button) );
        $(temp_table).append(last_row);
        return temp_table;
    }

    function add_user_to_collab(add_user_text_input, html_element_inside_collab) { // fix this
        collab_set_style_to(html_element_inside_collab, "processing");
        var collab_id = get_collab_id(html_element_inside_collab);
        var searchString = $(add_user_text_input).val();
        $.ajax({
            url: resolve_to_url["add_user_to_collab_url"],
            type: 'POST',
            data: {collab_id : collab_id, searchString : searchString},
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                var user_name_to_display = data["name_to_display"];
                var user_id = data["user_id"];
                add_row_to_authorized_users_table(user_id, user_name_to_display, html_element_inside_collab); // upon success in ajax
                collab_set_style_to(html_element_inside_collab, "editing"); // upon success in ajax

            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
                collab_set_style_to(html_element_inside_collab, "error");
            },
            async: true
        });
    }

    function remove_user_from_collab(user_id, html_element_inside_collab){ //finish this
        collab_set_style_to(html_element_inside_collab, "processing");
        var collab_id = get_collab_id(html_element_inside_collab);
        // make ajax call with collab_id and user_id
        $.ajax({
            url: resolve_to_url["remove_user_from_collab_url"],
            type: 'POST',
            data: {collab_id : collab_id, user_id : user_id},
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                remove_row_from_authorized_users_table(user_id); // upon success in ajax
                collab_set_style_to(html_element_inside_collab, "editing"); // upon success in ajax

            },
            error: function (jqXHR, textStatus, errorThrown) {
                //alert(jqXHR.responseText);
                collab_set_style_to(html_element_inside_collab, "error");
            },
            async: true
        });
    }

    function add_row_to_authorized_users_table(user_id, user_name_to_display, html_element_inside_collab) {
        var authorized_users_table = $("#settings_form").find(".authorized_users_table").get(0);
        var temp_row = $("<tr></tr>").attr("name", user_id);
        var remove_button = $("<button></button>").addClass("remove_user_from_collab").attr("name", user_id).text("Remove");
        $(remove_button).on("click", function(){ remove_user_from_collab(user_id, html_element_inside_collab) });
        $(temp_row).append( $("<td></td>").text(user_name_to_display) );
        $(temp_row).append( $("<td></td>").append(remove_button) );
        //var list_of_rows = $(authorized_users_table).children("tbody tr:last");
        var last_row = $(authorized_users_table).children("tbody").children("tr").last(); //$(list_of_rows).last();
        $(last_row).before(temp_row);
    }

    function remove_row_from_authorized_users_table(user_id) {
        var authorized_users_table = $("#settings_form").find(".authorized_users_table").get(0);
        var temp_row = $(authorized_users_table).find("tr[name=" + stripString(user_id.toString()) + "]").get(0);
        $(temp_row).remove();
    }

    function stripString(str) { // need to finish
        var stripped_string = str;
        return stripped_string;
    }

    $(".play_collab_button").click(play_collab);
    $(".restart_collab_button").click(restart_collab);

    /** ADD A DESCRIPTION */
    $(".remove_track_from_collab_button").click(function () {
        var this_button = this;
        var dialog_text = "Are you sure you want to remove this track from the collaboration?";
        var yes_func = function () {
           // var collab_DB_id = get_collab_id(this_button);
            //remove_track_from_collab(this_button.name, collab_DB_id);
            finalize_collaboration(this_button, "removed");
        };
        var no_func = function () {};
        confirm_dialog(dialog_text, yes_func, no_func);
    });

    //  function remove_track_from_collab(track_id, collab_id) {
    //    alert("track id: " + track_id + " " + "collab id: " + collab_id);
    //    $(this_button).bind("click", function(){ finalize_collaboration(this_button, "added") });
    //}

    /** ADD A DESCRIPTION */
    function play_collab() {
        var tracks_buttons = get_buttons_for_tracks_of_collab(this);
        $(tracks_buttons).each(function () {
            try{
                var music_player = get_music_player(this);
                play_music(music_player);
            } catch(e){
            }
        });
        collab_set_style_to(this, "play");
        $(this).off("click");
        $(this).on("click", pause_collab);
        $(this).text("Pause");
    }

    /** ADD A DESCRIPTION */
    function pause_collab() {
        var tracks_buttons = get_buttons_for_tracks_of_collab(this);
        $(tracks_buttons).each(function () {
            try{
                var music_player = get_music_player(this);
                pause_music(music_player);
            } catch(e) {
            }
        });
        collab_set_style_to(this, "pause");
        $(this).off("click");
        $(this).on("click", play_collab);
        $(this).text("Play");
    }

    /** ADD A DESCRIPTION */
    function restart_collab() {
        var tracks_buttons = get_buttons_for_tracks_of_collab(this);
        $(tracks_buttons).each(function () {
            try {
                var music_player = get_music_player(this);
                restart_music(music_player);
            } catch (e){
            }
        });
    }

    /** ADD A DESCRIPTION */
    function collab_set_style_to(html_element_inside_collab, style_type) {
        if (is_inside_collab(html_element_inside_collab)){
            var container_div = $(html_element_inside_collab).parents(".collab_div_container").get(0);
            style_type = style_type.toLowerCase();
            if (style_type == "play") {
                $(container_div).removeClass().addClass("collab_div_container collab_play");
            }
            else if (style_type == "processing") {
                $(container_div).removeClass().addClass("collab_div_container collab_processing");
            }
            else if (style_type == "editing") {
                $(container_div).removeClass().addClass("collab_div_container collab_editing");
            }
            else if (style_type == "error") {
                $(container_div).removeClass().addClass("collab_div_container collab_error");
            }
            else { // style_type == "pause"
                $(container_div).removeClass().addClass("collab_div_container collab_pause");
            }
        }
    }

    /** ADD A DESCRIPTION */
    function collab_get_style(html_element_inside_collab) {
        if (is_inside_collab(html_element_inside_collab)){
            var container_div = $(html_element_inside_collab).parents(".collab_div_container").get(0);
            var classes = $(container_div).attr("class").toLowerCase();
            if (classes.indexOf("collab_play") !== -1) {
                return "play";
            }
            else if (classes.indexOf("collab_processing") !== -1) {
                return "processing";
            }
            else if (classes.indexOf("collab_editing") !== -1) {
                return "editing";
            }
            else if (classes.indexOf("collab_error") !== -1) {
                return "error";
            }
            else { // classes.toLowerCase().index_of("collab_pause") !== -1
                return "pause"
            }
        }
    }

    /** ADD A DESCRIPTION */
    function get_buttons_for_tracks_of_collab(html_element){
        var container_div = $(html_element).parents(".collab_div_container").get(0);
        var collab_tracks_div = $(container_div).children(".collab_tracks_div").get(0);
        var tracks_buttons = $(collab_tracks_div).find(".show_hide_player_button");
        if (tracks_buttons){
            return tracks_buttons;
        }
    }

    $(".collab_tracks_div").hide();

    $(".collab_toggle_all_tracks").click(toggle_all_tracks);

    /** ADD A DESCRIPTION */
    function toggle_all_tracks(){
        var container_div = $(this).parents(".collab_div_container").get(0);
        if (container_div) {
            var collab_tracks_div = $(container_div)
                .children(".collab_tracks_div").get(0);
            var collab_users_div = $(container_div)
                .children(".collab_users_div").get(0);
            if (collab_tracks_div) {
                $(collab_users_div).toggle(500);
                $(collab_tracks_div).toggle(500);
            }
        }
    }

    $(".show_hide_player_button").click(show_player);

    /** ADD A DESCRIPTION */
    function show_player() {
        var music_player = get_music_player(this);
        if(!is_inside_collab(this)){
            play_music(music_player);
        }
        $(music_player).show(500);

        $(this).off("click");
        $(this).on("click", hide_player);
        $(this).text("Hide Player");
    }

    /** ADD A DESCRIPTION */
    function hide_player() {
        if (does_music_player_exist(this)) {
            var music_player = get_music_player(this);
            //pause_music(music_player);
            //$(music_player).hide(500);
            $(music_player).hide(500, function () {
                if (!is_inside_collab(this)) {
                    pause_music(music_player);
                }
            });
            //$(music_player).hide(500, function (){ remove_music_player(music_player);});

            $(this).off("click");
            $(this).on("click", show_player);
            $(this).text("Show Player");
        }
    }

    /** ADD A DESCRIPTION */
    function is_inside_collab(html_element) {
        if ($(html_element).parents(".collab_div_container").length == 0) {
            return 0;
        } else {
            return 1;
        }
    }

    /** ADD A DESCRIPTION */
    function get_collab_id(html_element) {
        if ($(html_element).parents(".collab_div_container").length == 0) {
            var attempt2 = get_selected_value_of_sibling_select_list(html_element, "collab_select_list");
            return attempt2;
        } else {
            return $(html_element).parents(".collab_div_container").get(0).id;
        }
    }


    /** ADD A DESCRIPTION */
    function create_music_player(audio_name) {
        var audio_div = $("<div></div>").addClass("audio_div").attr("name", audio_name);
        var temp_pathname = resolve_to_url["MEDIA_URL"] + audio_name;
        var audio_control = $("<audio></audio>").attr("controls", "");
        var source = $("<source></source>").attr("type", "audio/mpeg").attr("src", temp_pathname);
        audio_control.append(source);
        $(audio_control).on("play", function(){
            if (is_inside_collab(this)){
                collab_set_style_to(this, "play");
            }
        });
        $(audio_control).on("pause ended", function(event){
            if (event.type === "ended"){
                this.load();
                $(this).on("loadedmetadata", function(){
                    this.currentTime = 0;
                    this.pause();
                });
            }
            if (is_inside_collab(this)){
                var tracks_buttons = get_buttons_for_tracks_of_collab(this);
                var style_to_set = "pause";
                $(tracks_buttons).each(function () {
                    try{
                        var child_music_player = get_music_player(this);
                        var child_audio = $(child_music_player).children("audio").get(0);
                        if (!child_audio.paused && !child_audio.ended){
                            style_to_set = "play";
                            false; // does what "break;" does in OOP for/while loops
                        }
                    } catch(e) {
                    }
                });
                collab_set_style_to(this, style_to_set);
            }
        });
        audio_div.append(audio_control);
        return audio_div;
    }

    /** ADD A DESCRIPTION */
    function confirm_dialog(dialog_text, yes_funcToExecute, no_funcToExecute) {
        var dialog_box = $("<div></div>").appendTo("body").text(dialog_text);
        $(dialog_box).dialog({
            modal: true,
            height: 180,
            resizable: false,
            draggable: false,
            title: "Confirm",
            dialogClass: "confirm_dialog",
            open: function () {
                $(this).siblings('.ui-dialog-buttonpane').find('button:eq(1)').focus();
            },
            buttons: {
                "Yes": function () {
                    yes_funcToExecute();
                    $(this).dialog("close");
                },
                    "No": function () {
                    no_funcToExecute();
                    $(this).dialog("close");
                }
            },
            close: function (event, ui) {
                $(this).remove();
            }
        });
    }

    /** Creates a general dialog box using the parameters. */
    function create_dialog_box(dialog_html, title, width, height, action1_name, action2_name, action1_funcToExecute, action2_funcToExecute) {
        var dialog_box = $("<div></div>").appendTo("body").html(dialog_html);
        $(dialog_box).dialog({
            modal: true,
            height: height,
            width: width,
            resizable: false,
            draggable: false,
            title: title,
            dialogClass: "confirm_dialog",
            open: function () {
                $(this).siblings('.ui-dialog-buttonpane').find('button:eq(1)').focus();
            },
            buttons: {
                action1_name: function () {
                    action1_funcToExecute();
                    $(this).dialog("close");
                },
                action2_name: function () {
                    action2_funcToExecute();
                    $(this).dialog("close");
                }
            },
            close: function (event, ui) {
                $(this).remove();
            }
        });
    }

    /** ADD A DESCRIPTION */
    function remove_music_player(music_player) {
        $(music_player).remove();
    }

    /** ADD A DESCRIPTION */
    function does_music_player_exist(html_element) {
        var music_player = $(html_element).siblings(".audio_div");
        if (music_player.length != 0) {
            return 1;
        } else {
            return 0;
        }
    }

    /** ADD A DESCRIPTION */
    function get_music_player(html_element) {
        var music_player;
        if (does_music_player_exist(html_element)) {
            music_player = $(html_element).siblings(".audio_div").get(0);
            return music_player;
        } else {
            var parent = $(html_element).parent();
            music_player = create_music_player(html_element.name);
            $(music_player).hide();
            parent.append(music_player);
            return music_player;
        }
    }

    /** ADD A DESCRIPTION */
    function play_music(music_player) {
        var audio_control = $(music_player).children("audio").get(0);
        if (audio_control) {
            audio_control.play();
        }
    }

    /** ADD A DESCRIPTION */
    function pause_music(music_player) {
        var audio_control = $(music_player).children("audio").get(0);
        if (audio_control) {
            audio_control.pause();
        }
    }

    /** ADD A DESCRIPTION */
    function restart_music(music_player) {
        var audio_control = $(music_player).children("audio").get(0);
        if (audio_control) {
            audio_control.currentTime = 0;
            //play_music(music_player);
        }
    }

    /**
     * FUNCTIONALITY: Creates a new progress bar element.
     * INPUTS: 1) html_element: The html element to add the progress bar to.
     * OUTPUT: new_bar: The progress bar element.
     */
    function add_new_progress_bar(html_element) {
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
    function add_loading_track(preceding_text, element_to_add_before_to) {
        var temp = $("<li></li>").append(
        $("<span></span>").text(preceding_text + " "));
        var new_bar = add_new_progress_bar(temp);
        $(element_to_add_before_to).before(temp);
        return new_bar;
    }

    /**
    FUNCTIONALITY: Sets the length of the inner filling of the progress bar to visually indicate how much progress has been made.
     * INPUTS: 1) progress_bar: The progress bar to set the filling of.
     *         2) percent_0_to_100: The percent (range 0 to 100) of the progress bar that should be filled.
     * OUTPUT: None
     */
    function progress_bar_setPercent(progress_bar, percent_0_to_100) {
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
    function progress_bar_Failure(progress_bar) {
        $(progress_bar).children("div.progress_bar_inner").css("background-color", "red");
    }

    /** FUNCTIONALITY: An event handler used for the event of a file upload in progress. Updates the progress bar appropriately.
     * INPUTS: 1) evt: The event object.
     *         2) progress_bar: The progress bar to set the filling of.
     * OUTPUT: None
     */
    function progressHandler(evt, progress_bar) {
        if (evt.lengthComputable) {
            var percent_done = parseInt(100.0 * evt.loaded / evt.total);
            progress_bar_setPercent(progress_bar, percent_done);
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
    $('#id_file').change(function () {
        // gets the file from the file input and prepares it for uploading
        var form_data = new FormData();
        if (!$(this).val()) {
            return
        }
        var file_input = $(this)[0];
        var file = file_input.files[0];
        form_data.append('file', file);
        //form_data.append('user_email', '{{ user.email }}');

        // updates the UI to reflect a file which is uploading
        var new_bar = add_loading_track(file.name, $(this).parents(".tracks_list_authorized_buttons_item"));

        // updates the UI to allow the user to upload another file while the previous file is uploading
        $(this).parents("form").get(0).reset();

        // the ajax request to the server to upload the file
        $.ajax({
            url: resolve_to_url["upload_mp3_url"],
            type: 'POST',
            data: form_data,
            cache: false,        // tell the browser not to use its cache
            processData: false,  // we already have a FormData obj, so $ needs to leave it alone
            contentType: false,  // $ needs to leave the contentType alone
            xhr: function () {
                var xhr = jQuery.ajaxSettings.xhr();
                if (xhr.upload) {
                    xhr.upload.addEventListener('progress', function (evt) { progressHandler(evt, new_bar) }, false);
                    xhr.upload.addEventListener("error", function (evt) { uploadFailedHandler(evt, new_bar) }, false);
                }//if
                return xhr;
            },
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                server_filename = data["server_filename"];
                track_id = data["track_id"];
                update_completed_loading_track(new_bar, server_filename, track_id);

            },
            error: function (jqXHR, textStatus, errorThrown) {
                progress_bar_Failure(new_bar);
                alert(jqXHR.responseText);
            },
            async: true

        });
    });

    /** ADD A DESCRIPTION */
    function update_completed_loading_track(progress_bar, server_filename, track_id){
        var show_player_button = create_show_player_button(server_filename);
        var collaborate_button = create_collaborate_button(track_id);
		var edit_button = create_edit_button(track_id);
        var delete_track_button = create_delete_track_button(track_id);
        $(progress_bar).before(show_player_button);
        $(progress_bar).after(delete_track_button);
        $(progress_bar).after(" ");
        $(progress_bar).after(collaborate_button);
        $(progress_bar).after(" ");
		$(progress_bar).after(edit_button);
		$(progress_bar).after(" ");
        $(progress_bar).remove();
    }

    /** ADD A DESCRIPTION */
    function create_show_player_button(server_filename){
        var show_player_button = $("<button></button>").attr("name", server_filename);
        $(show_player_button).addClass("show_hide_player_button");
        $(show_player_button).text("Show Player");
        $(show_player_button).on("click", show_player);
        return show_player_button;
    }

    /** ADD A DESCRIPTION */
    function create_collaborate_button(track_id){
        var collaborate_button = $("<button></button>").attr("name", track_id);
        $(collaborate_button).addClass("collaborate_button");
        $(collaborate_button).text("Collaborate");
        $(collaborate_button).on("click", begin_collaboration);
        return collaborate_button;
    }



    /** ADD A DESCRIPTION */
    function create_delete_track_button(track_id){
        var delete_track_button = $("<button></button>").attr("name", track_id);
        $(delete_track_button).addClass("delete_track_from_server_button");
        $(delete_track_button).text("X");
        $(delete_track_button).on("click", delete_track_confirm_dialog);
        return delete_track_button;
    }


    $(".collaborate_button").click(begin_collaboration);


    /** ADD A DESCRIPTION */
    function begin_collaboration(){
        this_button = this;
        //var track1_id = $(this_button).attr("name");
        $.getJSON(resolve_to_url["get_tracks_for_current_user_JSON_url"], function (data) {
            var temp_select_input = turn_KV_data_into_select_input(data, "track_select_list");
            if (temp_select_input != null) {
                $(this_button).before(temp_select_input);
                $(this_button).text("Finalize Collaboration!");
                $(this_button).off("click");
                $(this_button).on("click", function(){ finalize_collaboration(this_button, "added") });
            }
        });
    }

	function create_edit_button(track_id) {
		var edit_button = $("<button></button>").attr("name", track_id);
		$(edit_button).addClass("edit_button");
		$(edit_button).text("Edit");
		$(edit_button).on("click",begin_edit);
		return edit_button;
	}

	$(".edit_button").click(begin_edit);


	function begin_edit() {
		var track_id = $(this).attr("name");
		window.location = resolve_to_url["editTrack_url"] + track_id;
	}

    /** ADD A DESCRIPTION */
    function finalize_collaboration(html_element, mod_type) {
        //this_button = this; = html_element
        var track1_id = get_track1_id(html_element);
        //var select_element = $(this_button).parent().children("select");
        //var track2_id = select_element.children(":selected").val();
        var track2_id = get_track2_id(html_element);
        var collab_id = get_collab_id(html_element);
        //alert("track1_id: " + track1_id + "track2_id: " + track2_id + "collab_id: " + collab_id + "mod_type: " + mod_type);
        collab_set_style_to(html_element, "processing");

        $.ajax({
            url: resolve_to_url["finalize_collaboration_url"],
            type: 'POST',
            data: {track1_id : track1_id, track2_id : track2_id, collab_id : collab_id, mod_type : mod_type},
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                location.reload();
                //update_collab(html_element, jqXHR.responseText);
                //collab_set_style_to(html_element, "pause");

            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
                collab_set_style_to(html_element, "error");
            },
            async: true

        });

    };

    /*
    function update_collab(html_element, new_collab_html){
        var new_collab_list_element = $("<li></li>").html(new_collab_html);
        //collab_bind_all(new_collab_list_element);

        var old_container_div = $(html_element).parents(".collab_div_container").get(0);
        var old_collab_list_element = $(old_container_div).parent();

        if (typeof old_container_div != "undefined"){
            var next_sibling_list_element = $(old_collab_list_element).next()[0];
            if (typeof next_sibling_list_element == "undefined"){
                //$(old_collab_list_element).remove();
                var ul_element = $(old_collab_list_element).parents();
                $(ul_element).append(new_collab_list_element);
            } else {
                $(old_collab_list_element).remove();
                $(next_sibling_list_element).before(new_collab_list_element);
            }
        } else {
            collab_set_style_to(html_element, "error");
        }
    }


    function collab_bind_all(new_collab_list_element){

    }
    */

    /** ADD A DESCRIPTION */
    function get_track1_id(html_element){
        return $(html_element).attr("name");
    }

    /** ADD A DESCRIPTION */
    function get_track2_id(html_element){
        return get_selected_value_of_sibling_select_list(html_element, "track_select_list");
    }

    /** ADD A DESCRIPTION */
    function get_selected_value_of_sibling_select_list(html_element, class_of_select_list){
        var select_element;
        if (typeof class_of_select_list === "undefined") {
            return undefined;
        } else {
            select_element = $(html_element).siblings("select"+"."+class_of_select_list);
        }
        var selected_value = select_element.children(":selected").val();
        return selected_value;
    }

    /** ADD A DESCRIPTION */
    function turn_KV_data_into_select_input(data, class_string, selected_option) {
        if (data == null || data.length == 0 || data == '{}') {
            return null
        }
        var temp_select_input = $("<select></select>").addClass(class_string);
        if (typeof selected_option !== "undefined"){
            selected_option = selected_option.toLowerCase();
        }

        /* key is value and val is text (as opposed to the more common sense way of key is text and val is value).
           This counterintuitive method is used because keys need to be unique, which means that they are often id's of objects from the server.
           However, when submitting a form, it is the value which is processed by the server, so making value an id allows for the server to get
           an unique identifier. */
        $.each(data, function (key, val) {
            var temp_value = key.toString().toLowerCase();
            var temp_text = val.toString();
            var temp_choice = $("<option></option>");
            $(temp_choice).attr("value", temp_value);
            $(temp_choice).text(temp_text);
            if (temp_value == selected_option){
                $(temp_choice).attr("selected", "")
            }
            $(temp_select_input).append(temp_choice);
        });

        return temp_select_input;
    }

    $(".delete_track_from_server_button").click(delete_track_confirm_dialog);

    function delete_track_confirm_dialog(){
        var this_button = this;
        var dialog_message = "Are you sure you want to permanently delete this track? This process is irreversible!";
        confirm_dialog(dialog_message, function() { delete_track_from_server(this_button) }, function(){});
    }

    function delete_track_from_server(html_element){
        var track_id = get_track1_id(html_element);
        $.ajax({
            url: resolve_to_url["delete_track_from_server_url"],
            type: 'POST',
            data: {track_id : track_id},
            success: function (data, textStatus, jqXHR) {
                //alert(jqXHR.responseText);
                var track = get_tracks_list_item(html_element);
                $(track).remove();
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert(jqXHR.responseText);
            },
            async: true

        });
    }

    function get_tracks_list_item(html_element){
        return $(html_element).parents(".tracks_list_item");
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

});