var doc = app.activeDocument;

function rasterize(){
    doc.selectObjectsOnActiveArtboard();
    app.executeMenuCommand("Rasterize 8 menu item");
}

function offsetPath(){
    doc.artboards.setActiveArtboardIndex(0);
    doc.selectObjectsOnActiveArtboard();
    var sel = doc.selection;
    var lastObj = sel[sel.length - 1];
    lastObj.strokeColor = new NoColor();
    if(lastObj.filled == true){
        xmlstring = "<LiveEffect name=\"Adobe Offset Path\"><Dict data=\"R mlim 4 R ofst 11.5 I jntp 2\"/></LiveEffect>"; 
        lastObj.applyEffect(xmlstring);
    }
}

function clearArtboard(){
    if(doc.selection.length < 1){
        alert("none");
    }
    else{
        app.executeMenuCommand("cut");
        doc.selectObjectsOnActiveArtboard();
        var objects = doc.selection;
        for (i = objects.length - 1; i >= 0; i--) {
            var item = objects[i];
            item.remove();
    }
    app.executeMenuCommand("pasteInPlace");
    }
}

function resizeArtboard(){
    doc.selectObjectsOnActiveArtboard();
    doc.fitArtboardToSelectedArt(0);
    var rect = [
        doc.artboards[0].artboardRect[0] - 50,
        doc.artboards[0].artboardRect[1] + 50,
        doc.artboards[0].artboardRect[2] + 50,
        doc.artboards[0].artboardRect[3] - 50
    ]
    doc.artboards[0].artboardRect = rect;
}

function artboardDuplicate(){
    var thisBoardIndex = doc.artboards.getActiveArtboardIndex();
    var thisBoard = doc.artboards[thisBoardIndex];
    var thisRect = thisBoard.artboardRect;
    var lastBoard = doc.artboards[doc.artboards.length - 1];
    var lastRect = lastBoard.artboardRect;
    doc.selectObjectsOnActiveArtboard();
    app.copy();
    var newBoard = doc.artboards.add(thisRect);
    var offsetH = 20;
    newBoard.artboardRect = [
        lastRect[2] + offsetH,
        lastRect[1],
        lastRect[2] + offsetH + (thisRect[2] - thisRect[0]),
        lastRect[3]
    ];
    newBoard.name = thisBoard.name + " copy";
    app.executeMenuCommand("pasteFront");
    doc.selection = null;
};
function itemDeleteExceptLast(){
    doc.artboards.setActiveArtboardIndex(1);
    doc.selectObjectsOnActiveArtboard();
    var objects = doc.selection;
    for (i = objects.length - 1; i >= 0; i--) {
        var item = objects[i];
        if(i === objects.length - 1){
            var col = new CMYKColor();
            col.cyan = 0;
            col.magenta = 0;
            col.yellow = 0;
            col.black = 100;
            var swatch = doc.swatches.add();
            swatch.color = col;
            swatch.name = "col";
            item.filled = true;
            item.fillColor = swatch.color;
            item.strokeColor = new NoColor();
            item.opacity = 100;
            continue;
        }
        item.remove();
    }
}

if(doc.selection.length < 4){
    alert("Zaznacz cala etykiete");
}
else{
    app.executeMenuCommand("cut");
    activeDocument.selectObjectsOnActiveArtboard();
    var objects = doc.selection;
    for (i = objects.length - 1; i >= 0; i--) {
        var item = objects[i];
        item.remove();
    }
    app.executeMenuCommand("pasteInPlace");
    resizeArtboard();
    artboardDuplicate();
    itemDeleteExceptLast();
    offsetPath();
    rasterize();
}


