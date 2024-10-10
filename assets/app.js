window.my_tools = Object.assign({}, window.my_tools, {
    hasClass : function(obj, cls) {  
        return obj.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));  
    },
    addClass : function(obj, cls) {  
        if (!window.my_tools.hasClass(obj, cls)) obj.className += " " + cls;  
    },
    removeClass: function(obj, cls) {  
        if (window.my_tools.hasClass(obj, cls)) {  
            var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');  
            obj.className = obj.className.replace(reg, ' ');  
        }  
    } ,
    toggleClass: function(obj,cls){  
        if(window.my_tools.hasClass(obj,cls)){  
            window.my_tools.removeClass(obj, cls);  
        }else{  
            window.my_tools.addClass(obj, cls);  
        }  
    },
    launchFullScreen: function(element) {
        if(element.requestFullscreen) {
            element.requestFullscreen();
        } else if(element.mozRequestFullScreen) {
            element.mozRequestFullScreen();
        } else if(element.webkitRequestFullscreen) {
            element.webkitRequestFullscreen();
        } else if(element.msRequestFullscreen) {
            element.msRequestFullscreen();
        }
    },
    exitFullscreen: function() {
        if(document.exitFullscreen) {
            document.exitFullscreen();
        } else if(document.mozExitFullScreen) {
        document.mozExitFullScreen();
        } else if(document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
    },
    plotFullScreen: function(fig,conf){
        var icon = {
            'width': 512,
            'height': 512,
            'path': "M512 512v-208l-80 80-96-96-48 48 96 96-80 80z M512 0h-208l80 80-96 96 48 48 96-96 80 80z M0 512h208l-80-80 96-96-48-48-96 96-80-80z M0 0v208l80-80 96 96 48-48-96-96 80-80z"
        }
        conf["modeBarButtonsToAdd"] = [
            {
                name: 'Full Screen',
                icon: icon,
                click: function(gd) {
                    if (!document.fullscreenElement){
                        var update = {
                            showlegend: true,
                            legend:{
                                title:""
                            }
                        }
                        Plotly.relayout(gd, update)
                        window.my_tools.launchFullScreen(gd)
                    } else{
                        var update = {
                            showlegend: false
                        }
                        Plotly.relayout(gd, update)
                        window.my_tools.exitFullscreen()
                    }
                }
            }
        ]
        
        return conf
    }
});





