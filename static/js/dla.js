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
    var $container = $('.filter_container').isotope({
        layoutMode: 'vertical',
        filter: '.page_1'
    });

    var $map_container = $('.map_filter_container').isotope({
        layoutMode: 'fitRows',
    });

    // reset isotopes filters
    $("#filter_reset_btn").click(function () {
        $map_container.isotope({ filter: "" });
        map.setZoom(2);
        $("#current_filter").html("");
        $("#filter_reset_btn").css( "display", "none");
    });

    // page filter
    $(".page_filter_selector").click(function () {
        $(".filter_selected").removeClass("filter_selected");
        $(this).addClass("filter_selected");

        var f =  $(this).attr('data-filter');
        $container.isotope({ filter: f });
        $("#curr_page_filter").html($(this).attr('name')+" ("+$(f).length);
    });

    // record filter
    $(".record_filter_selector").click(function () {
        $(".filter_selected").removeClass("filter_selected");
        $(this).addClass("filter_selected");
        var f =  $(this).attr('data-filter');
        $container.isotope({ filter: f });
        $("#curr_page_filter").html($(this).attr('name')+" ("+$(f).length);
    });

    // language filter
    $(".mapped_language_selector").click(function () {
        if( $(this).hasClass("map_language_selected") ) {
            $(this).removeClass("map_language_selected");
            $map_container.isotope({ filter: "" });
            $("#filter_reset_btn").css( "display", "none");
        } else {
            $(".map_language_selected").removeClass("map_language_selected");
            $(this).addClass("map_language_selected");
            var f = "."+$(this).html();
            $map_container.isotope({ filter: f });
            $("#filter_reset_btn").css( "display", "inline");
        }
    });

    // show infowindow in the google map for a selected collection in list of mapped collections
    $(".mapped_collection_selector").click(function () {
        // Toggle infowindow control from dom elements.
        if( $(this).hasClass("filter_selected") ) {
            $(this).removeClass("filter_selected");
            map.setZoom(2);
            $("#filter_reset_btn").css( "display", "none");
            infowindow.close(map);
        } else {
            var lat = $(this).children(".latitude").val();
            var lng = $(this).children(".longitude").val();

            // grab the relevant info from hidden inputs to display in infowindow
            var collection_name = $(this).children(".collection").val();
            var collection_url = $(this).children(".site_url").val();
            var languages = $(this).children(".language").val();
            var display_text = '<p><b>Collection: </b><a href=\"' + collection_url + '\">' + collection_name + '</a>' + '<br><b>Language: </b> ' + languages + '<br><b>Coordinates: </b>Latitude: ' + lat + ', Longitude: ' + lng + '</p>';


            var infowindowOptions = {
                content: display_text,
                position: {lat: parseFloat(lat), lng: parseFloat(lng)},
                maxWidth: 200
            };
            infowindow.setOptions(infowindowOptions);
            infowindow.open(map);


            $(".filter_selected").removeClass("filter_selected");
            $(this).addClass("filter_selected");
            $("#filter_reset_btn").css( "display", "inline");
        }
    });

    // show infowindow in the google map for a selected record in list of mapped records
    $(".mapped_record_selector").click(function () {
        // Toggle infowindow control from dom elements.
        if( $(this).hasClass("filter_selected") ) {
            $(this).removeClass("filter_selected");
            $("#filter_reset_btn").css( "display", "none");
            infowindow.close(map);
        } else {
            var lat = $(this).children(".latitude").val();
            var lng = $(this).children(".longitude").val();

            // grab the relevant info from hidden inputs to display in infowindow
            var collection_name = $(this).children(".collection").val();
            var collection_url = $(this).children(".site_url").val();
            var languages = $(this).children(".language").val();
            var display_text = '<p><b>Collection: </b><a href=\"' + collection_url + '\">' + collection_name + '</a>' + '<br><b>Language: </b> ' + languages + '<br><b>Coordinates: </b>Latitude: ' + lat + ', Longitude: ' + lng + '</p>';


            var infowindowOptions = {
                content: display_text,
                position: {lat: parseFloat(lat), lng: parseFloat(lng)},
                maxWidth: 200
            };
            infowindow.setOptions(infowindowOptions);
            infowindow.open(map);


            $(".filter_selected").removeClass("filter_selected");
            $(this).addClass("filter_selected");
            $("#filter_reset_btn").css( "display", "inline");
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
            var pivot=actual_page*10;
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
        paginator();
    });

});