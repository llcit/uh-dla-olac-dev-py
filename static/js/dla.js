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
            var display_text = '<p><b>Collection: </b><a href=\"' + $(this).children(".site_url").val() + '\">' + $(this).children(".title").val() + '</a>' + 
                '<br><b>Language: </b> ' + $(this).children(".language").val() + 
                '<br><b>Coordinates: </b> ' + lat + ', ' + lng + '</p>';
            
            var center = new google.maps.LatLng(lat, lng);
            var infowindowOptions = {
                content: display_text,
                position: center,
                maxWidth: 150
            };
            
            infowindow.setOptions(infowindowOptions);
            infowindow.open(map);

            // Add a marker for the plot to the map.
            // var marker = new google.maps.Marker({
            //       position: center,
            //       map: map,
            // });

            // Set up event listener for markers: when clicked will filter mapped records list.
            // google.maps.event.addListener(marker, 'click', function() {
            //     map.setZoom(12);
            //     map.setCenter(this.getPosition());

            //     // normalize the position strings with the dom class specified in mapped records.
            //     var latstr = String(this.getPosition().lat()).replace('.', '').slice(0,6);
            //     var lngstr = String(this.getPosition().lng()).replace('.', '').slice(0,6);
                
            //     // build string used to select relevant classes from mapped records list
            //     var record_filter = ".coord"+latstr +"_"+lngstr;
            //     // console.log(record_filter);
            //     // display the collection title currently being filtered / handle the button to reset filter
            //     $("#filter_reset_btn").css( "display", "inline");
            //     $("#current_filter").html( $(record_filter).first().children(".collection").val() )

            //     // Finally, let isotope do its magic.
            //     $container.isotope({ filter: record_filter });                 
            // });


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
                return 0;       
            }

            var mapPlots = [];
            for (var i = 0; i<json.length; i++) {
                mapPlots[i] = new google.maps.LatLng(json[i].east, json[i].north );
                console.log('Plot at: ' + "LAT: " + json[i].east + " LONG: " + json[i].north);
                console.log('Plot at: ' + mapPlots[i]);
            }

            if (typeof mapPlots[0] != 'undefined') {
                // k=longitude (north)
                // B=latitude (east)
                var mapcenter = new google.maps.LatLng(mapPlots[0].B, mapPlots[0].k);
            } else {
                var mapcenter = new google.maps.LatLng(0, 0);
            }

            var mapOptions = {
                zoom: 1,
                minZoom:1,
                center: mapcenter,
                mapTypeId: google.maps.MapTypeId.SATELLITE
            };

            map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);


            for (var i = 0; i<mapPlots.length; i++) {
                // Add a marker for each plot to the map.
                console.log('Marker at: ' + mapPlots[i]);
                new google.maps.Marker({
                      position: {lat: mapPlots[i].B, lng: mapPlots[i].k},
                      map: map,
                });
                
                // // Set up event listener for markers: when clicked will filter mapped records list.
                // google.maps.event.addListener(marker, 'click', function() {
                //     map.setZoom(12);
                //     map.setCenter(this.getPosition());

                //     // normalize the position strings with the dom class specified in mapped records.
                //     var latstr = String(this.getPosition().lat()).replace('.', '').slice(0,6);
                //     var lngstr = String(this.getPosition().lng()).replace('.', '').slice(0,6);
                    
                //     // build string used to select relevant classes from mapped records list
                //     var record_filter = ".coord"+latstr +"_"+lngstr;
                //     // console.log(record_filter);
                //     // display the collection title currently being filtered / handle the button to reset filter
                //     $("#filter_reset_btn").css( "display", "inline");
                //     $("#current_filter").html( $(record_filter).first().children(".collection").val() )

                //     // Finally, let isotope do its magic.
                //     $container.isotope({ filter: record_filter });                 
                // });
            }

            // Init 'global' infowindow object set to blank.
            infowindow = new google.maps.InfoWindow({ content: "" }); 
            
            // set up infowindow to modify dom relevant dom elements when close button is clicked.
            google.maps.event.addListener(infowindow, 'closeclick', function() {
                $(".map_collection_selected").removeClass("map_collection_selected");
            });

            return map;
        }

        // Init Google map (or not)
        initialize();
        // paginator();
    });

});




// window.onload = loadScript;