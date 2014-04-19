/**
 * Created with PyCharm.
 * User: Julian Jaffe
 * Date: 4/18/14
 * Time: 2:58 PM
 * To change this template use File | Settings | File Templates.
 */

function LoadTracks(){
    this.buffer = null;
    this.cb = null;
    this.init = function init(cb) {
        // Fix up prefixing
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        context = new AudioContext();
        this.cb = cb;

        bufferLoader = new BufferLoader(
            context,
            [
                "http://127.0.0.1:8000/Tracks/user_mp3_files/2_04-16-2014_09-48-27.mp3"
            ],
            finishedLoading
        );

        bufferLoader.load();

        cb.onFinish;

    }

    function finishedLoading(bufferList) {
        this.buffer = bufferList[0];
        // Create two sources and play them both together.
        //filedb = new FileDropbox();
        //blob = new Blob(bufferList, {type: "audio/wav"});
        //FileDropbox(bufferlist, filedb);
        //FileDropbox.handleFiles(bufferList,filedb);
        /*var source1 = context.createBufferSource();
         source1.buffer = bufferList[0];

         source1.connect(context.destination);
         source1.start(0);                           // play the source now*/

    }
}
