
var data = {};
var property_names = [];
var properties = [];
var n_class = 3;

window.onload = function() {
    var data_str = document.getElementById("data").innerHTML;
    var find = "\'";
    var re = new RegExp(find, 'g');
    data_str = data_str.replace(re, "\"");
    // console.log(data_str);

    data = JSON.parse(data_str);

    if ( window.location.pathname == "/settings" || window.location.pathname == "/new" ) {
        property_names = data.worker_property_names;
        properties = data.worker_properties;
        n_class = data.worker_properties[0].length;

        if (data.data_selection != "default") {
            document.getElementById("tg1").checked = false;
            document.getElementById("tg2").checked = true;
        }
        if (data.task_assignment != "default") {
            document.getElementById("ta1").checked = false;
            document.getElementById("ta2").checked = true;
        }
        if (data.worker_selection != "none") {
            document.getElementById("ws1").checked = false;
            document.getElementById("ws2").checked = true;
        }
        showproperties();
    }
    else if ( window.location.pathname == "/plugins" ) {
        if (data.data_selection == "default") {
            document.getElementById("taskgen").style.display = "none";
        }
        if (data.task_assignment == "default") {
            document.getElementById("taskassign").style.display = "none";
        }
        if (data.worker_selection == "none") {
            document.getElementById("workerslt").style.display = "none";
        }
    }
    else if (window.location.pathname == "/results" ) {
        var str = "";
        for ( var i = 0 ; i < data["output"].length ; i ++ ) {
            var prop = data["output"][i].replace(".png","");
            str += "<center><b>Results of <i>"+prop+"</i></b><br>";
            str += "<img src=\"fig?pid="+data["pid"]+"&prop="+prop+"\" style=\"width:70%;\"></img></center><br><br><hr>";
        }
        document.getElementById("qualityres").innerHTML = str;
    }
}

function datasettings() {
    window.location.hash = "#datasettings";
}

function workersettings() {
    window.location.hash = "#workersettings";
}

function outputsettings() {
    window.location.hash = "#outputsettings";
}

function pluginssettings() {
    window.location.hash = "#plugins";
}

function newproperties() {
    n_class = parseInt(document.getElementById("n_class").value);
    if ( n_class < 1 ) n_class = 1;
    if ( n_class > 5 ) n_class = 5;
    property_names = ["class_name","distribution","execution_time"];
    properties = [[],[],[]];
    for ( var i = 0 ; i < n_class ; i ++ ) {
        properties[0][i] = "class"+(i+1);
        properties[1][i] = 1/n_class;
        properties[2][i] = (i+1) * 100;
    }
    showproperties();
}

function showproperties() {
    var table = "<center><table>";
    for ( var i = 0 ; i < property_names.length ; i ++ ) {
        table += "<tr><td style=\"height:20px;\"></td>";
        table += "<td style=\"height:20px;\"><span style=\"font-size:12px;\">"+property_names[i]+"</span></td>";
        for ( var j = 0 ; j < n_class ; j ++ ) {
            table += "<td style=\"height:20px;\"><input id=\"p"+i+"_"+j+"\" style=\"font-size:12px;\" size=\"20\" value=\""+properties[i][j]+"\"></td>";
        }
        table += "</tr>";
    }
    table += "</center></table>";
    document.getElementById("properties").innerHTML = table;
    document.getElementById("properties").style.display = "block";
}

function updateproperty() {
    for ( var i = 0 ; i < property_names.length ; i ++ ) {
        for ( var j = 0 ; j < n_class ; j ++ ) {
            properties[i][j] = document.getElementById("p"+i+"_"+j).value;
        }
    }
}

function showaddproperty() {
    updateproperty();
    document.getElementById("property_name").value = "property name";
    document.getElementById("add_prop").style.display = "inline-block";
}

function addproperty() {
    updateproperty();
    var p = document.getElementById("property_name").value;
    if ( property_names.indexOf(p) < 0 && p!="property name") {
        property_names.push(p);
        properties.push([]);
        showproperties();
        document.getElementById("add_prop").style.display = "none";
    }
}

function get_radio_value(name) {
    var radios = document.getElementsByName(name);
    for (var i = 0, length = radios.length; i < length; i++)
        if (radios[i].checked) return radios[i].value;
    return "";
}

function savebtn_settings() {
    var newDate = new Date();
    var datetime = newDate.toLocaleString();
    updateproperty();

    var settings = {
        "title": document.getElementById("data-title").value,
        "pid": document.getElementById("data-pid").innerHTML,
        "file": document.getElementById("file").value,
        "price": document.getElementById("price").value,
        "n_judgements": document.getElementById("n_judgements").value,
        "worker_arrival_interval":  document.getElementById("worker_arrival_interval").value,
        "dropout_time":  document.getElementById("dropout_time").value,
        "worker_classification": properties[0].length,
        "worker_property_names": property_names,
        "worker_properties": properties,
        "runtime": document.getElementById("runtime").value,
        "time_stamp": document.getElementById("time_stamp").value,
        "repeat_times": document.getElementById("repeat_times").value,
        "n_data_rows": document.getElementById("n_data_rows").value,
        "created": document.getElementById("data-created").innerHTML,
        "modified": datetime,
        "data_selection": get_radio_value("tg"),
        "task_assignment": get_radio_value("ta"),
        "worker_selection": get_radio_value("ws")
    };
    jQuery.ajax({
        url: "/save",
        type: "POST",
        contentType: "application/json",
        // crossDomain: true,
        data: JSON.stringify(settings),
        dataType: "json",
        success:function(response){
            console.log(response);
        },
        error:function(e){
            console.log(e);
        }
    });
}


function savebtn_plugins() {

    var functions = {
        "pid": document.getElementById("data-pid").innerHTML,
        "workermodel": ace.edit("editor1").getValue(),
        "taskmodel": ace.edit("editor2").getValue(),
        "workerslt": ace.edit("editor3").getValue(),
        "taskgen": ace.edit("editor4").getValue(),
        "taskassign": ace.edit("editor5").getValue(),
        "others": ace.edit("editor6").getValue()
    };
    jQuery.ajax({
        url: "/savefunc",
        type: "POST",
        contentType: "application/json",
        // crossDomain: true,
        data: JSON.stringify(functions),
        dataType: "json",
        success:function(response){
            console.log(response);
        },
        error:function(e){
            console.log(e);
        }
    });
}

function gotopage_settings(url) {
    var newDate = new Date();
    var datetime = newDate.toLocaleString();
    updateproperty();

    var settings = {
        "title": document.getElementById("data-title").value,
        "pid": document.getElementById("data-pid").innerHTML,
        "file": document.getElementById("file").value,
        "price": document.getElementById("price").value,
        "n_judgements": document.getElementById("n_judgements").value,
        "worker_arrival_interval":  document.getElementById("worker_arrival_interval").value,
        "dropout_time":  document.getElementById("dropout_time").value,
        "worker_classification": properties[0].length,
        "worker_property_names": property_names,
        "worker_properties": properties,
        "runtime": document.getElementById("runtime").value,
        "time_stamp": document.getElementById("time_stamp").value,
        "repeat_times": document.getElementById("repeat_times").value,
        "n_data_rows": document.getElementById("n_data_rows").value,
        "created": document.getElementById("data-created").innerHTML,
        "modified": datetime,
        "data_selection": get_radio_value("tg"),
        "task_assignment": get_radio_value("ta"),
        "worker_selection": get_radio_value("ws")
    };
    jQuery.ajax({
        url: "/save",
        type: "POST",
        contentType: "application/json",
        // crossDomain: true,
        data: JSON.stringify(settings),
        dataType: "json",
        success:function(response){
            console.log(response);
            window.location.href = url;
        },
        error:function(e){
            window.location.href = url;
        }
    });
}


function gotopage_plugins(url) {

    var functions = {
        "pid": document.getElementById("data-pid").innerHTML,
        "workermodel": ace.edit("editor1").getValue(),
        "taskmodel": ace.edit("editor2").getValue(),
        "workerslt": ace.edit("editor3").getValue(),
        "taskgen": ace.edit("editor4").getValue(),
        "taskassign": ace.edit("editor5").getValue(),
        "others": ace.edit("editor6").getValue()
    };
    jQuery.ajax({
        url: "/savefunc",
        type: "POST",
        contentType: "application/json",
        // crossDomain: true,
        data: JSON.stringify(functions),
        dataType: "json",
        success:function(response){
            console.log(response);
            window.location.href = url;
        },
        error:function(e){
            console.log(e);
            window.location.href = url;
        }
    });
}


function gotopage(url) {
    window.location.href = url;
}


function runbtn() {
    if ( window.location.pathname == "/plugins" ) savebtn_plugins();
    else savebtn_settings();

    document.getElementById("run-button").style.visibility = "hidden";
    document.getElementById("stop-run").style.visibility = "visible";
    document.getElementById("run-cover").style.display = "block";
    jQuery.ajax({
        url: "/run?pid="+data.pid,
        success:function(response){
            console.log(response);
                document.getElementById("run-button").style.visibility = "visible";
                document.getElementById("stop-run").style.visibility = "hidden";
                document.getElementById("run-cover").style.display = "none";
        },
        error:function(e){
            console.log(e);
        }
    });
}
