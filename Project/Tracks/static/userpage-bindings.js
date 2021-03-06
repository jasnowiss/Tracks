
/* THE SCRIPT THAT WAS PREVIOSULY AT THE END OF USERPAGE.HTML HAS BEEN SPLIT INTO TWO .JS FILES
** THIS FILE CONTAINS ALL THE EVENT BINDINGS, ETC. WHICH WERE PREVIOUSLY IN USERPAGE.HTML */

$(document).ready(function () {

  /********************************** Functions of NISHANT KUMAR ***************************************/

    //$(document).tooltip();
    $(".settings_button").click(open_settings);
    $("#settings_div").hide();

    $(".play_collab_button").click(play_collab);
    $(".restart_collab_button").click(restart_collab);

    $(".remove_track_from_collab_button").click(remove_track_from_collab);

    $(".collab_tracks_div").hide();

    $(".collab_toggle_all_tracks").click(toggle_all_tracks);

    $(".show_hide_player_button").click(show_player);

    $('.musicUpload input[type="file"]').change(upload_file);

    $(".collaborate_button").click(begin_collaboration);

	$(".edit_button").click(begin_edit);

    $(".delete_track_from_server_button").click(delete_track_confirm_dialog);

    $("#test").click(function(){ update_collab(this); });

   // $(".loading_gif").css("visibility", "hidden");

    setTimeout(function(){ run_collab_updates($(".collab_last_known_update").get(0)); }, 5000);

    /*$(".collab_div_container").on("load", function(){});*/
    $.each($(".collab_div_container"), function(index, value){
        initialize_collab_sliders(value);
    });

});