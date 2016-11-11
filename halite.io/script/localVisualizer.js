$(function () {
    var $dropZone = $("#dropZone");
    $("#pageContent").append($dropZone);

    $dropZone.on('dragover', function(e) {
        e.stopPropagation();
        e.preventDefault();
    });
    $dropZone.on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
        var files = e.originalEvent.dataTransfer.files; // Array of all files
        for(var i=0, file; file=files[i]; i++) {
            console.log(file)
            var reader = new FileReader();

            reader.onload = (function(filename) { // finished reading file data.
                return function(e2) {
                    $dropZone.remove();
                    showGame(textToGame(e2.target.result, filename), true, false); 
                };
            })(file.name);
            reader.readAsText(file); // start reading the file data.
        }
    });
})
