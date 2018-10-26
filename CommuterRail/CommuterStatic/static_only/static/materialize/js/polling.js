/**
 * Retrieve cookie from browser
 * @param {string} c_name 
 * Credits to: https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
 */
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$(document).ready(function() {
    /*** Live Polling of Data
     * This function will poll every minute and update the page every 15 seconds
     * A proper implementation would be to add proper sockets, subscribe to alerts, or to use MBTA's own even streaming
     * In order to keep the complexity of the project relatively simple, opted for a simple 1 minute polling solution
     */
    var cookie = getCookie("csrftoken");
    if (cookie.length === 0) {
        // M.toast({html: "No cookies!"});
        cookie = document.getElementById('cookieToken').innerHTML; //Handle weird situations where people don't have cookies enabled
    }

    setInterval(function() {
    $.ajax({
        headers: { "X-CSRFToken": cookie},
        url: "/page-info/",
        type:"POST",
        success: function( data ) {
            //console.log("yay")
            document.getElementById('time').innerHTML = data["time"]
            document.getElementById('date').innerHTML = data["date"]
            document.getElementById('today').innerHTML = data["today"]
            var predictionsNorth = data["north_station"];
            var predictionsSouth = data["south_station"];
            

            if ("north_station" in data) {
                var north_station_innerHTML = "";

                Object.keys(predictionsNorth).forEach(function(key) {
                    var prediction = predictionsNorth[key];
                    var td_beg = "<td>";
                    var td_end = "</td>";
                    if (prediction.platform_code === null) {
                        prediction.platform_code = "TBD"
                    }
                    var departure_time = td_beg + prediction.departure_time + td_end;
                    var headsign = td_beg + prediction.headsign + td_end;
                    var train_number = td_beg + prediction.train_number + td_end;
                    var platform_code = td_beg + prediction.platform_code + td_end;
                    var status = td_beg + prediction.status + td_end;
                    var innerHTML = "<tr>" + departure_time + headsign + train_number + platform_code + status + "</tr>"
                    north_station_innerHTML += innerHTML;
                    //console.log(key, predictionsNorth[key]);
                });

                document.getElementById('northStationBody').innerHTML = north_station_innerHTML;
            } 

            if ("south_station" in data) {
                var south_station_innerHTML = "";

                Object.keys(predictionsSouth).forEach(function(key) {
                    var prediction = predictionsSouth[key];
                    var td_beg = "<td>";
                    var td_end = "</td>";
                    if (prediction.platform_code === null) {
                        prediction.platform_code = "TBD"
                    }
                    var departure_time = td_beg + prediction.departure_time + td_end;
                    var headsign = td_beg + prediction.headsign + td_end;
                    var train_number = td_beg + prediction.train_number + td_end;
                    var platform_code = td_beg + prediction.platform_code + td_end;
                    var status = td_beg + prediction.status + td_end;
                    innerHTML = "<tr>" + departure_time + headsign + train_number + platform_code + status + "</tr>"
                    south_station_innerHTML += innerHTML;
                    //console.log(key, predictionsSouth[key]);
                });

                document.getElementById('southStationBody').innerHTML = south_station_innerHTML;
            } 

            // M.toast({html: "Data Refreshed!"});
        },
        error: function(xhr, status, error) {
            //console.log("error")
            // M.toast({html: "There was an error!"});
            // Could have put cookie logic here, but then would fail first and then go here
        },
        // dataType : "json"
        }).done(function(data){
            //Can do some extra work if needed...
        });
    }, 15 * 1000);
});