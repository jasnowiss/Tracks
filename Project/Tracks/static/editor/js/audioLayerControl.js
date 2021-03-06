function audioLayerControl(elementContext)
{
    // the context of the hosting element
    this.elementContext = elementContext;
    this.elementContext.audioLayerControl = this;
    
    // HTML attributes
    this.title = "untitled";

    // HTML subelements
    this.label = undefined;
    /**
     * @type AudioSequenceEditor
     * @var Audio
     */
    this.audioPlayer = undefined;
    
    //
    this.listOfSequenceEditors = [];
    this.linkMode = false;
    
    // total length of the longest sequence
    this.audioSequenceLength = 0;
    
    this.playLoop = false;

    // use the audio context to play audio
    this.audioPlayback = new AudioPlayback();
    
    this.audioPlayback.addUpdateListener(this);

    this.spectrum = new SpectrumDisplay(this.elementContext, $('#spectrum')[0]);    
    this.spectrumWorker = new SpectrumWorker();
    
    this.audioPlaybackUpdate = function audioPlaybackUpdate()
    {
        for (var i = 0; i < this.listOfSequenceEditors.length; ++i)
        {
            this.listOfSequenceEditors[i].playbackPos = this.audioPlayback.currentPlayPosition;
            this.listOfSequenceEditors[i].repaint();
        }
        
        var frequencyDomain = new Float32Array(this.audioPlayback.analyserNode.frequencyBinCount);
        this.audioPlayback.analyserNode.getFloatFrequencyData(frequencyDomain);
        this.spectrum.updateBuffer(frequencyDomain);
        this.spectrum.paintSpectrum();
    };
    
    this.audioSequenceSelectionUpdate = function audioSequenceSelectionUpdate()
    {
        var dataLength = this.listOfSequenceEditors[0].audioSequenceReference.data.length;
        var start = this.listOfSequenceEditors[0].selectionStart;
        start = (start < 0) ? 0 :
            (start > this.listOfSequenceEditors[0].audioSequenceReference.data.length - 1024) ?
            this.listOfSequenceEditors[0].audioSequenceReference.data.length - 1024 : start;
        
        var len = ((this.listOfSequenceEditors[0].selectionEnd > dataLength) ? dataLength : this.listOfSequenceEditors[0].selectionEnd) - start;

        var frequencyAmplitude = this.spectrumWorker.toAmplitudeSpectrumFromAudioSequence(
                                                                                          this.listOfSequenceEditors[0].audioSequenceReference,
                                                                                          start,
                                                                                          len);
        
        this.spectrum.updateBuffer(frequencyAmplitude);
        this.spectrum.paintSpectrum();

    };
    
    // Properties    
    this.setTitle = function setTitle(titleValue)
    {
        this.title = titleValue;
        //this.label.innerHTML = this.title;
    };
    
    this.containsAudioLayerSequenceEditor = function containsAudioLayerSequenceEditor(name)
    {
        for (var i = 0; i < this.listOfSequenceEditors.length; ++i)
        {
            if (this.listOfSequenceEditors[i].title == name) return true;
        }
        return false;
    };
    
    this.addAudioLayerSequenceEditor = function addAudioLayerSequenceEditor(audioLayerSequenceEditor)
    {
        for (var i = 0; i < this.listOfSequenceEditors.length; ++i)
        {
            if (this.listOfSequenceEditors[i].title === audioLayerSequenceEditor.title) return;
        }
        this.listOfSequenceEditors.push(audioLayerSequenceEditor);
        
        this.updateLinkMode(this.linkMode);
    };
    
    this.removeAudioLayerSequenceEditor = function removeAudioLayerSequenceEditor(audioLayerSequenceEditor)
    {
        for (var i = 0; i < this.listOfSequenceEditors.length; ++i)
        {
            if (this.listOfSequenceEditors[i].title === audioLayerSequenceEditor.title)
            {
                this.listOfSequenceEditors.splice(i, 1);
            }
        }
        
        this.updateLinkMode(this.linkMode);
    };
    
    this.updateLinkMode = function updateLinkMode(linkModeValue)
    {
        this.linkMode = linkModeValue;
        if (this.linkMode)
        {
            for(var i = 0; i < this.listOfSequenceEditors.length - 1; ++i)
            {
                for(var j = i + 1; j < this.listOfSequenceEditors.length; ++j)
                {
                    this.listOfSequenceEditors[i].link(this.listOfSequenceEditors[j]);
                }   
            }
        }
        else
        {
            
        }
    };
    
    // Create visual elements of this html element
    // Visual Elements
    this.createVisualElements = function createVisualElements()
    {
        /*this.label = document.createElement("label");
        this.label.innerHTML = this.title;
        this.elementContext.appendChild(this.label);
        */
        /*
        this.audioPlayer = document.createElement("Audio");
        this.audioPlayer.controls = true;
        this.elementContext.appendChild(this.audioPlayer);*/
    };
    
    this.createVisualElements();
    
    // Scan for attributes of the HTML element during the creation
    if ((typeof elementContext.attributes.title !== undefined) &&
        elementContext.attributes.title !== null)
    {
        this.setTitle(elementContext.attributes.title.value);
    }    
    
    // public functions
    this.createSequenceEditor = function createSequenceEditor(name)
    {
        if (this.audioLayerControl.containsAudioLayerSequenceEditor(name) === true) return undefined;
        
        var sequenceEditorElement = document.createElement("audioLayerSequenceEditor");
        sequenceEditorElement.title = name;
        this.appendChild(sequenceEditorElement);
        var obj = new AudioLayerSequenceEditor(sequenceEditorElement);
        this.audioLayerControl.addAudioLayerSequenceEditor(obj);
        return obj;
    };
    
    this.removeAllSequenceEditors = function removeAllSequenceEditors()
    {
        for (var i = 0; i < this.children.length; ++i)
        {
            if (this.children[i].nodeName.toLowerCase() == "audiolayersequenceeditor")
            {
                this.audioLayerControl.removeAudioLayerSequenceEditor(this.children[i].audioLayerSequenceEditor);
                this.removeChild(this.children[i]);
                --i;
            }
        }
    };    
    
    this.setLinkMode = function setLinkMode(linkModeValue)
    {
        this.audioLayerControl.updateLinkMode(linkModeValue);
    };
    
    this.zoomIntoSelection = function zoomIntoSelection()
    {
        if (this.audioLayerControl.listOfSequenceEditors.length > 0 && this.linkMode)
        {
            this.audioLayerControl.listOfSequenceEditors[0].zoomIntoSelection();
        }
        else
        {
            for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
            {
                this.audioLayerControl.listOfSequenceEditors[i].zoomIntoSelection();
            }
        }
    };
    
    this.zoomToFit = function zoomToFit()
    {
        if (this.audioLayerControl.listOfSequenceEditors.length > 0 && this.linkMode)
        {
            this.audioLayerControl.istOfSequenceEditors[0].zoomIntoSelection();
        }
        else
        {
            for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
            {
                this.audioLayerControl.listOfSequenceEditors[i].zoomToFit();
            }
        }
    };
    
    this.selectAll = function selectAll()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].selectAll();
        }
    };
    
    this.filterNormalize = function filterNormalize()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].filterNormalize();
        }  
    };
    
    this.filterFadeIn = function filterFadeIn()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].filterFade(true);
        }  
    };
    
    this.filterFadeOut = function filterFadeOut()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].filterFade(false);
        }  
    };
    
    this.filterGain = function filterGain(decibel)
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].filterGain(decibel);
        } 
    };
    
    this.filterSilence = function filterSilence()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].filterSilence();
        } 
    };
    
    this.copy = function copy()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].copy(false);
        } 
    };
    
    this.paste = function paste()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].paste(false);
        } 
    };
    
    this.cut = function cut()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].cut(false);
        } 
    };
    
    this.del = function del()
    {
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].del(false);
        } 
    };
    
    // in und export
    this.toWave = function toWave()
    {
        var wave = new WaveTrack();
        var sequenceList = [];
        
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            sequenceList.push(this.audioLayerControl.listOfSequenceEditors[i].audioSequenceReference);
        }
        
        wave.fromAudioSequences(sequenceList);
        return wave;
    }
    
    this.playToggle = function playToggle()
    {
        if (this.audioLayerControl.audioPlayback.isPlaying)
        {
            this.stop();
        }
        else
        {
            this.play();
        }
    };
    
    // playback
    this.play = function play()
    {
        // fast version (only chrome)
        var audioDataRefs = [];
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            audioDataRefs.push(this.audioLayerControl.listOfSequenceEditors[i].audioSequenceReference.data);
        }
        
        var selectionStart = this.audioLayerControl.listOfSequenceEditors[0].selectionStart;
        var selectionEnd = this.audioLayerControl.listOfSequenceEditors[0].selectionEnd;
        if (selectionStart != selectionEnd)
        {
            this.audioLayerControl.audioPlayback.play(audioDataRefs,
                                                  this.audioLayerControl.listOfSequenceEditors[0].audioSequenceReference.sampleRate, this.playLoop,
                                                  selectionStart, selectionEnd);
        }
        else
        {
            this.audioLayerControl.audioPlayback.play(audioDataRefs,
                                                  this.audioLayerControl.listOfSequenceEditors[0].audioSequenceReference.sampleRate, this.playLoop);
        }
        
        
        /* slow version
        this.toWave().toBlobUrlAsync("audio/wav", function(url, host)
                                {
                                    host.audioLayerControl.audioPlayer.src = url;
                                    host.audioLayerControl.audioPlayer.play();
                                }, this);
        */  
    };
    
    this.stop = function stop()
    {
        console.log("Stop");
        this.audioLayerControl.audioPlayback.stop();
        //this.audioLayerControl.stopFromAudioContext();
        //this.audioLayerControl.audioPlayer.pause();   
    };
    
    this.toggleLoop = function toogleLoop()
    {
        this.playLoop = !this.playLoop;
    };

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }
    var csrf_token = getCookie('csrftoken');

    this.save = function save(saveLink)
    {
        var blob = this.toWave().toBlob("application/octet-stream");
        var filename = this.title.substring((this.title.lastIndexOf('/')) + 1);
        var data = new FormData();
        data.append('csrfmiddlewaretoken', csrf_token);
        data.append('filename', filename);
        data.append("audio", blob);
        $.ajax({
          url :  "/Tracks/handleRecord",
          type: 'POST',
            data: data,
            contentType: false,
            processData: false,
            success: function(data) {
                //Redirect? Modify UI in place? Notify User?
                console.log("Saved.");
            },
            error: function() {
                //Notify User, or ignore if no recording?
                console.log("Failed.");
            }
        });
        /*var url = this.toWave().toBlobUrlAsync("application/octet-stream");
        saveLink.href = url;
        saveLink.className = "btn btn-large btn-success";
        /*this.toWave().toBlobUrlAsync(function(url, host)
                                {
                                    saveLink.href = url;
                                }, saveLink);  */
    };
    
    this.testFilter = function testFilter()
    {// audioLayerControl
        var audioDataRefs = [];
        for(var i = 0; i < this.audioLayerControl.listOfSequenceEditors.length; ++i)
        {
            audioDataRefs.push(this.audioLayerControl.listOfSequenceEditors[i].audioSequenceReference.data);
        }
        
        for (var i = 0; i < audioDataRefs.length; ++i)
        {
            this.audioLayerControl.listOfSequenceEditors[i].audioSequenceReference.data = this.audioLayerControl.spectrumWorker.testFilter(audioDataRefs[i]);
        }
        
        this.zoomToFit();

    };
    
    this.createTestSignal = function createTestSignal()
    {
        this.removeAllSequenceEditors();
        
        var numChannels = 2;
        for (var i = 0; i < numChannels; ++i)
        {
            var editor = this.createSequenceEditor("Test Channel " + i);
            var sequence = CreateNewAudioSequence(44100);
            sequence.createTestTone(44100 / 1024 * 10, 44100 * 10);
            editor.setAudioSequence(sequence);
            editor.zoomToFit();
        }   
    };
    
    // Match functions for HTML Element
    this.elementContext.createSequenceEditor = this.createSequenceEditor;
    this.elementContext.removeAllSequenceEditors = this.removeAllSequenceEditors;
    this.elementContext.setLinkMode = this.setLinkMode;
    this.elementContext.zoomIntoSelection = this.zoomIntoSelection;
    this.elementContext.zoomToFit = this.zoomToFit;
    this.elementContext.selectAll = this.selectAll;
    
    this.elementContext.filterNormalize = this.filterNormalize;
    this.elementContext.filterFadeIn = this.filterFadeIn;
    this.elementContext.filterFadeOut = this.filterFadeOut;
    this.elementContext.filterGain = this.filterGain;
    this.elementContext.filterSilence = this.filterSilence;
    
    this.elementContext.toWave = this.toWave;
    this.elementContext.playToggle = this.playToggle;
    this.elementContext.play = this.play;
    this.elementContext.stop = this.stop;
    this.elementContext.toggleLoop = this.toggleLoop;
    this.elementContext.save = this.save;
    this.elementContext.testFilter = this.testFilter;
    this.elementContext.createTestSignal = this.createTestSignal;
    
    this.elementContext.copy = this.copy;
    this.elementContext.paste = this.paste;
    this.elementContext.cut = this.cut;
    this.elementContext.del = this.del;
    
    // Drag and Drop
    this.filedb = undefined;

    /*function LoadTracks(){
        this.buffer = null;
        this.init = function init() {
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

        }

        function finishedLoading(bufferList) {
            this.buffer = bufferList[0];
        }
    }*/


    /*var loader = new LoadTracks();
    loader.init();
    this.eventHost.audioPlayback.audioContext.decodeAudioData(loader.buffer, this.eventHost.decodeAudioFinished, this.eventHost.decodeAudioFailed);
    */
    /*this.loader = undefined;
    this.load = function load(){
        var loader = function() { LoadTracks() };
        loader.init();
        loader.eventHost = this;

        loader.onFinish = function()
        {
            $('#app-progress')[0].style['width'] = '50%';
            activeAudioLayerControl = this.eventHost.elementContext;
            this.eventHost.audioPlayback.audioContext.decodeAudioData(this.buffer, this.eventHost.decodeAudioFinished, this.eventHost.decodeAudioFailed);
        }
    }

    this.load();*/

    this.loader = function load(url){
        var request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.responseType = 'arraybuffer';
        request.eventHost = this;

        // Decode asynchronously
        request.onload = function() {

            activeAudioLayerControl = this.eventHost.elementContext;
            this.eventHost.audioPlayback.audioContext.decodeAudioData( request.response, this.eventHost.decodeAudioFinished, this.eventHost.decodeAudioFailed);
        }
        request.send();
    }

    this.loader(this.title);

    this.createDropHandler = function createDropHandler()
    {
        var filedb = new FileDropbox();
        filedb.defineDropHandler(this.elementContext);
		console.log(this.elementContext);
        filedb.eventHost = this;

        filedb.onFinish = function()
        {
            $('#app-progress')[0].style['width'] = '50%';
            activeAudioLayerControl = this.eventHost.elementContext;
            this.eventHost.audioPlayback.audioContext.decodeAudioData(this.resultArrayBuffer, this.eventHost.decodeAudioFinished, this.eventHost.decodeAudioFailed);
        }

        filedb.onFail = function(e)
        {
            var msg = '';


            switch (e.target.error.code) {
              case FileError.QUOTA_EXCEEDED_ERR:
                msg = 'QUOTA_EXCEEDED_ERR';
                break;
              case FileError.NOT_FOUND_ERR:
                msg = 'NOT_FOUND_ERR';
                break;
              case FileError.SECURITY_ERR:
                msg = 'SECURITY_ERR';
                break;
              case FileError.INVALID_MODIFICATION_ERR:
                msg = 'INVALID_MODIFICATION_ERR';
                break;
              case FileError.INVALID_STATE_ERR:
                msg = 'INVALID_STATE_ERR';
                break;
              default:
                msg = 'Unknown Error ' + e.code;
                break;
            };

            console.log('Error: ' + msg);
        }
    };
    
    this.decodeAudioFinished = function decodeAudioFinished(audioBuffer)
    {
        $('#app-progress')[0].style['width'] = '90%';

        activeAudioLayerControl.removeAllSequenceEditors();
        
        var sampleRate = audioBuffer.sampleRate; // samples per second (float)
        var length = audioBuffer.length; // audio data in samples (float)
        var duration = audioBuffer.duration; // in seconds (float)
        var numChannels = audioBuffer.numberOfChannels; // (unsigned int)
        
        var channelNames = ["Left Channel", "Right Channel"];
        
        for (var i = 0; i < numChannels; ++i)
        {
            var editor = activeAudioLayerControl.createSequenceEditor(channelNames[i]);
            var sequence = CreateNewAudioSequence(sampleRate, audioBuffer.getChannelData(i));
            editor.setAudioSequence(sequence);
            editor.zoomToFit();
        }
        
        //activeAudioLayerControl.audioLayerControl.setupAudioContext();
        $('#app-progress')[0].style['width'] = '100%';
        
        setTimeout(function() { $('#app-progress')[0].style['width'] = '0%'; }, 1000);
    };

    /*this.createDropHandler();*/
    
    this.elementContext.onselectstart = function() { return(false); };
    
}

function initializeAudioLayerControls()
{
    new audioLayerControl(document.getElementsByTagName("audiolayercontrol")[0]);

    //var allElements = document.getElementsByTagName("audiolayercontrol");
    /*for(var i = 0; i < allElements.length; ++i)
    {
        var tagName = allElements[i].nodeName;
        console.log(tagName + " " + i);
        var obj = null;
        
        if (tagName.toLowerCase() == "audiolayercontrol")
        {
            obj = new audioLayerControl(allElements[i]);   
        }
        else if (tagName.toLowerCase() == "audiolayernavigation")
        {
            obj = new audioLayerControl(allElements[i]);   
        }
        else if (tagName.toLowerCase() == "audiolayersequenceeditor")
        {
            obj = new AudioLayerSequenceEditor(allElements[i]);   
        }
    }*/
}

var activeAudioLayerControl = undefined;
