//Script to create the map.
var map = L.map('mapid').setView([-40, 0], 2);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 20,
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox.streets',
  accessToken: 'your.mapbox.access.token'
}).addTo(map);

//Allowing drawing tools
var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);

var drawControl = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false
    },
    draw: {
        polyline: false,
        polygon: false,
        circle: false,
        marker: false,
        rectangle: true
    }
});

map.addControl(drawControl);

//Edit drawing tools
var drawControlEditOnly = new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        edit: false
    },
    draw: false
});

//Variable which will become the coordinates to send to GEE
coords_to_send = ""

//Function that gets the coordinates and return a string in URL parameter format.
function getStringCords(object_coords){
  var coords = "la1="+object_coords[0].lat+"&lo1="+object_coords[0].lng
  coords += "&la2="+object_coords[1].lat+"&lo2="+object_coords[1].lng
  coords += "&la3="+object_coords[2].lat+"&lo3="+object_coords[2].lng
  coords += "&la4="+object_coords[3].lat+"&lo4="+object_coords[3].lng
  return coords;
}

//Remove draw control tools and add edit control tools
map.on("draw:created", function (e) {
    var layer = e.layer;
    var roi = layer
    var coords = layer.getLatLngs()
    coords_to_send = getStringCords(coords[0]);
    layer.addTo(drawnItems);
    drawControl.remove(map);
    drawControlEditOnly.addTo(map);
});


//When the rectangle is deleted, add again drawing tools
map.on("draw:deleted", function(e) {
    coords_to_send = "";
    drawControlEditOnly.remove(map);
    drawControl.addTo(map);
});

//Button functionality
$( "#redirect" ).click(function() {
  if(coords_to_send != ""){
    window.location.href = "./hello?" + coords_to_send
  }
});
