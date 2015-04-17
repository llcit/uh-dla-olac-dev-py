// map-init.js

jQuery(function($) {

	$(document).ready(function() {
		function initialize_map() {
		    var mapPlots = [];
		    // See this link to understand why north is mapped to the x coordinate (latitude) and east is mapped to y coordinate (longitude)
		    // https://developers.google.com/maps/documentation/javascript/reference#LatLng
		    for (var i = 0; i<json.length; i++) {
		        mapPlots[i] = new google.maps.LatLng(json[i].north, json[i].east );
		        // console.log('Plot at: ' + "LAT: " + json[i].east + " LONG: " + json[i].north);
		        // console.log('Plot at: ' + mapPlots[i]);
		    }

		    // var mapcenter = new google.maps.LatLng(19.50056, 155.50056);
		    // var mapOptions = {
		    //     zoom: 2,
		    //     minZoom:1,
		    //     center: mapcenter,
		    //     mapTypeId: google.maps.MapTypeId.SATELLITE
		    // };

		    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);


		    for (var i = 0; i<mapPlots.length; i++) {
		        // Add a marker for each plot to the map.
		        var marker =  new google.maps.Marker({
		              position: mapPlots[i],
		              map: map,
		        });

		        // Set up event listener for markers: when clicked will filter mapped records list.
		        google.maps.event.addListener(marker, 'click', function() {
		            map.setZoom(12);
		            map.setCenter(this.getPosition());

		            // normalize the position strings with the dom class string specified in mapped objects.
		            var latstr = String(this.getPosition().lat()).replace('.', '').slice(0,6);
		            var lngstr = String(this.getPosition().lng()).replace('.', '').slice(0,6);

		            // build string used to select relevant classes from mapped collections list
		            var map_filter = ".coord"+latstr +"_"+lngstr;


		            // Trigger the filter (isotope) code : see dla.js
		            if($(map_filter).length) {
		            	$(map_filter).click();
		            } // No corresponding filter is setup in the dom or not found the build the infowindow here.
		            else {
			            // grab the relevant info from hidden inputs to display in infowindow
			            var collection_name = $(map_filter).first().children(".collection").val();
			            var collection_url = $(map_filter).first().children(".site_url").val();
			            var languages = $(map_filter).first().children(".language").val();
			            var display_text = '<p><b>Collection: </b><a href=\"' + collection_url + '\">' + collection_name + '</a>' + '<br><b>Coordinates: </b><br>Latitude: ' + this.getPosition().lat() + ', Longitude: ' + this.getPosition().lng() + '</p>';


			            var infowindowOptions = {
			                content: display_text,
			                position: this.getPosition(),
			                maxWidth: 200
			            };
			            infowindow.setOptions(infowindowOptions);
			            infowindow.open(map);
		            }

		        });
		    }

		    infowindow = new google.maps.InfoWindow();

		    // set up infowindow to modify dom relevant dom elements when close button is clicked.
		    google.maps.event.addListener(infowindow, 'closeclick', function() {
		        $(".filter_selected").removeClass("filter_selected");
		    });

		    return map;
		}

		// Init Google map (or not)
		if (json.length < 1){
            $("#map-canvas").toggle();
            $("#nogeotext").toggle();
            $("#mapped_collection_selector").toggle();
        } else {
	        initialize_map();
		}
	});
});