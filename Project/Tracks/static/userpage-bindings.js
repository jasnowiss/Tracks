
/* THE SCRIPT THAT WAS PREVIOSULY AT THE END OF USERPAGE.HTML HAS BEEN SPLIT INTO TWO .JS FILES
** THIS FILE CONTAINS ALL THE EVENT BINDINGS, ETC. WHICH WERE PREVIOUSLY IN USERPAGE.HTML */

$(document).ready(function () {

  /********************************** Functions of NISHANT KUMAR ***************************************/

    $(".settings_button").click(open_settings);
    $("#settings_div").hide();

    $(".play_collab_button").click(play_collab);
    $(".restart_collab_button").click(restart_collab);

    $(".remove_track_from_collab_button").click(remove_track_from_collab);

    $(".collab_tracks_div").hide();

    $(".collab_toggle_all_tracks").click(toggle_all_tracks);

    $(".show_hide_player_button").click(show_player);

    $('.musicUpload input[name="file"]').change(upload_file);

    $(".collaborate_button").click(begin_collaboration);

	$(".edit_button").click(begin_edit);

    $(".delete_track_from_server_button").click(delete_track_confirm_dialog);

});