// dla.js
var map;
var infowindow;

//DOM Variables
    var collection_items = $(" #collection .list-group").children();
    var collection_pages = Math.ceil(collection_items.length/10);
    var language_items = $(" #language .list-group").children();
    var language_pages = Math.ceil(language_items.length/10);
    var depositor_items = $(" #depositor .list-group").children();
    var depositor_pages = Math.ceil(depositor_items.length/10);
    //We store the page it is being showned for each group Collection, Language, Depositor initially 1. First Page
    var collection_pager=1;
    var depositor_pager=1;
    var language_pager=1;
    var first_cut=10;

//############# End of Variables declaration ################# 

jQuery(function($) {
    // init Isotope
    var $container = $('.mapitem_container').isotope({
        layoutMode: 'fitRows',
    });

    // reset isotopes filters
    $("#filter_reset_btn").click(function () {
        $container.isotope({ filter: "" });
        map.setZoom(2);
        $("#current_filter").html("");
        $("#filter_reset_btn").css( "display", "none");
        $(".map_language_selected").removeClass("map_language_selected");   
    });

    // language filter
    $(".mapped_language_selector").click(function () {
        if( $(this).hasClass("map_language_selected") ) {
            $(this).removeClass("map_language_selected");
            $container.isotope({ filter: "" });
            $("#filter_reset_btn").css( "display", "none");
        } else {
            $(".map_language_selected").removeClass("map_language_selected");
            $(this).addClass("map_language_selected");
            var f = "."+$(this).html();
            $container.isotope({ filter: f });
            $("#filter_reset_btn").css( "display", "inline");
        }        
    });

    // show infowindow in the google map for a selected record in list of mapped records
    $(".mapped_collection_selector").click(function () {
        // Toggle infowindow control from dom elements.
        if( $(this).hasClass("map_collection_selected") ) {
            $(this).removeClass("map_collection_selected");
            infowindow.close(map);
        } else {
            var lat = $(this).children(".latitude").val();
            var lng = $(this).children(".longitude").val();
            
            // grab the relevant info from hidden inputs to display in infowindow
            var collection_name = $(this).children(".collection").val();
            var collection_url = $(this).children(".site_url").val();
            var languages = $(this).children(".language").val();
            var display_text = '<p><b>Collection: </b><a href=\"' + collection_url + '\">' + collection_name + '</a>' + '<br><b>Language: </b> ' + languages + '<br><b>Coordinates: </b>east: ' + lat + ', north: ' + lng + '</p>';

            
            var infowindowOptions = {
                content: display_text,
                position: {lat: parseFloat(lat), lng: parseFloat(lng)},
                maxWidth: 200
            };                    
            infowindow.setOptions(infowindowOptions);
            infowindow.open(map);


            $(".map_collection_selected").removeClass("map_collection_selected");
            $(this).addClass("map_collection_selected");
        }
    });

    $(document).ready(function() {

        function paginator () {
            //Initially we show 10 elements of each group
            collection_items.slice(first_cut,collection_items.length).hide();
            language_items.slice(first_cut,language_items.length).hide();
            depositor_items.slice(first_cut,depositor_items.length).hide();

            //Click Handlers
            $(".previous .collection").click(function(){
                if(collection_pager!=1){
                    collection_pager--;
                    $("#next_col").removeClass("disabled");
                    showItems(collection_pager,collection_pages,"#prev_col",collection_items,"prev");
                }
            });
            $(".next .collection").click(function(){
                if(collection_pager!=collection_pages){
                    collection_pager++;
                    $("#prev_col").removeClass("disabled");
                    showItems(collection_pager,collection_pages,"#next_col",collection_items,"next");
                }
            });
            $(".previous .language").click(function(){
                if(language_pager!=1){
                    language_pager--;
                    $("#next_lan").removeClass("disabled");
                    showItems(language_pager,language_pages,"#prev_lan",language_items,"prev");
                }
            });
            $(".next .language").click(function(){
                if(language_pager!=language_pages){
                    language_pager++;
                    $("#prev_lan").removeClass("disabled");
                    showItems(language_pager,language_pages,"#next_lan",language_items,"next");
                }
            });
            $(".previous .depositor").click(function(){
                if(depositor_pager!=1){
                    depositor_pager--;
                    $("#next_dep").removeClass("disabled");
                    showItems(depositor_pager,depositor_pages,"#prev_dep",depositor_items,"prev");
                }
            });
            $(".next .depositor").click(function(){
                if(depositor_pager!=depositor_pages){
                    depositor_pager++;
                    $("#prev_dep").removeClass("disabled");
                    showItems(depositor_pager,depositor_pages,"#next_dep",depositor_items,"next");
                }
            });
        }

        function showItems (actual_page,num_pages,elements,collection,type){
            var pivot=actual_page*10;;
            //last page
            if(actual_page==num_pages){
                $(elements).addClass("disabled");
                collection.slice(pivot-10,collection.length).show();
                collection.slice(0,pivot-10).hide();
            }
            //middle pages
            if(actual_page<num_pages && actual_page!=1){
                if(type=="next"){
                    collection.slice(pivot-10,pivot).show();
                    collection.slice(0,pivot-10).hide();
                    collection.slice(pivot,collection.length).hide();
                }else{ //type previous
                    collection.slice(pivot-10,pivot).show();
                    collection.slice(0,pivot-10).hide();
                    collection.slice(pivot,collection.length).hide();
                }
                

            }
            //first page
            if(actual_page==1){
                $(elements).addClass("disabled");
                collection.slice(0,pivot).show();
                collection.slice(pivot ,collection.length).hide()  ; 
            }
        }

        function initialize() {
            if (json.length < 1){
                $("#map-canvas").toggle();
                $("#nogeotext").toggle();
                $("#mapped_collection_selector").toggle();
                return       
            }

            var mapPlots = [];
            // See this link to understand why north is mapped to the x coordinate (latitude) and east is mapped to y coordinate (longitude)
            // https://developers.google.com/maps/documentation/javascript/reference#LatLng
            for (var i = 0; i<json.length; i++) {
                mapPlots[i] = new google.maps.LatLng(json[i].north, json[i].east );
                // console.log('Plot at: ' + "LAT: " + json[i].east + " LONG: " + json[i].north);
                // console.log('Plot at: ' + mapPlots[i]);
            }

            if (typeof mapPlots[0] != 'undefined') {
                // k=longitude (north)
                // B=latitude (east)
                var mapcenter = mapPlots[0]
            } else {
                var mapcenter = new google.maps.LatLng(0, 0);
            }

            var mapOptions = {
                zoom: 2,
                minZoom:1,
                center: mapcenter,
                mapTypeId: google.maps.MapTypeId.SATELLITE
            };

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

                    // normalize the position strings with the dom class specified in mapped records.
                    var latstr = String(this.getPosition().lat()).replace('.', '').slice(0,6);
                    var lngstr = String(this.getPosition().lng()).replace('.', '').slice(0,6);
                    
                    // build string used to select relevant classes from mapped collections list
                    var map_filter = ".coord"+lngstr +"_"+latstr;

                    // grab the relevant info from hidden inputs to display in infowindow
                    var collection_name = $(map_filter).first().children(".collection").val();
                    var collection_url = $(map_filter).first().children(".site_url").val();
                    var languages = $(map_filter).first().children(".language").val();
                    var display_text = '<p><b>Collection: </b><a href=\"' + collection_url + '\">' + collection_name + '</a>' + '<br><b>Language: </b> ' + languages + '<br><b>Coordinates: </b>east: ' + this.getPosition().lat() + ', north: ' + this.getPosition().lng() + '</p>';

                    
                    var infowindowOptions = {
                        content: display_text,
                        position: this.getPosition(),
                        maxWidth: 200
                    };                    
                    infowindow.setOptions(infowindowOptions);
                    infowindow.open(map);

                    // Display the reset button -- 'show all'
                    $("#filter_reset_btn").css( "display", "inline");
                    
                    // Finally, let isotope do its magic.
                    $container.isotope({ filter: map_filter });

                });
                        
                        
            }
                 
            infowindow = new google.maps.InfoWindow();

            // set up infowindow to modify dom relevant dom elements when close button is clicked.
            google.maps.event.addListener(infowindow, 'closeclick', function() {
                $(".map_collection_selected").removeClass("map_collection_selected");
            });

            return map;
        }

        // Init Google map (or not)
        initialize();
        paginator();
    });

});




// window.onload = loadScript;