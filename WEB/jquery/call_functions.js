function saveModel(){
    var params = document.getElementsByName("paramModel");
    var modelParams = [];
    

    params.forEach(
        function(currentValue){
            modelParams.push(currentValue.value);
        }
    );

    ajaxRequest("POST", "http://ihm.tradingbot.business/methods.php", "json", "saveModel" , modelParams);

}

function addSymbol(){

    var id = document.getElementById("formId");
    var name = document.getElementById("formName");
    var mtid = document.getElementById("formMtId");
    var secteur = document.getElementById("formSecteur");
    var supersecteur = document.getElementById("formSuperSecteur");
    var pays = document.getElementById("formPays");
    var active = document.getElementById("formActive");

    var params = [id.value, name.value, mtid.value, secteur.value, supersecteur.value, pays.value, active.checked];

    ajaxRequest("POST", "http://ihm.tradingbot.business/methods.php", "json", "addSymbol" , params);
}

function actionSymbol(id_symbol, action){
    var params = [id_symbol, action];
    ajaxRequest("POST", "http://ihm.tradingbot.business/methods.php", "json", "udpateSymbol" , params); 
}

function getNews(){

    var select = document.getElementById("selectCompany")
    var company = select.options[select.selectedIndex].text;
    
    ajaxRequest("POST", "http://ihm.tradingbot.business/methods.php", "json", "getNews" , company); 
}

function displayNews(news){

    newsDiv = document.getElementById("divNews");
    newsDiv.innerHTML = "";

    if(news["count"] > 0){
        
        for (const index in news["objects"]) {
            colsm = document.createElement("div");
            colsm.setAttribute("class", "col-sm");
            
            card = document.createElement("div");
            card.setAttribute("class", "card");
            card.style.width = "20rem";

            image = document.createElement("img");
            image.src = news["objects"][index]["urlToImage"];
            image.setAttribute("class", "card-img-top");

            cardbody = document.createElement("div");
            cardbody.setAttribute("class", "card-body");
            
            title = document.createElement("h5");
            title.innerHTML = news["objects"][index]["title"];
            title.setAttribute("class", "card-title");
            title.style.minHeight = "100px";

            date = 

            description = document.createElement("p");
            description.setAttribute("class", "card-text");
            description.innerHTML = news["objects"][index]["description"];
            description.style.minHeight = "200px";

            button = document.createElement("a");
            button.className = "btn";
            button.className += " btn-primary";
            button.href = news["objects"][index]["url"];
            button.innerHTML = "Lire l'article";
            button.style.margin = "auto";
            button.target = "_blank";


            cardbody.appendChild(title);
            cardbody.appendChild(description);
            cardbody.appendChild(button);

            card.appendChild(image);
            card.appendChild(cardbody);
            colsm.appendChild(card);
            newsDiv.appendChild(colsm);

            if(index == 2){
                break;
            }
        }
    }else{
        oups = document.createElement("h3");
        oups.innerHTML = "Pas d'actualité trouvée pour cette entreprise";
        oups.style.textAlign = "center";
        oups.style.color = "#C2C2C2";

        newsDiv.appendChild(oups);

    }



    
}

function buildGraphBalance(balance){

    var lowest = Number.POSITIVE_INFINITY;
    var highest = Number.NEGATIVE_INFINITY;
    var tmp;
    for (var i=balance.length-1; i>=0; i--) {
        tmp = balance[i].y;
        if (tmp < lowest) lowest = tmp;
        if (tmp > highest) highest = tmp;
    }

    console.log(lowest);
    console.log(highest);
    var chart = new CanvasJS.Chart("chartBalance", {
		title:{
			text: "Evolution de la balance"              
        },
        axisY:{
            minimum: lowest - 10,
            maximum: highest + 10,
            title: "Euros",
           },
        axisX:{
            title: "Date"
        },
		data: [              
		{
			// Change type to "doughnut", "line", "splineArea", etc.
			type: "line",
			dataPoints: balance
		}
		]
	});
	chart.render();

}

function buildGraphEquity(equity){

    var lowest = Number.POSITIVE_INFINITY;
    var highest = Number.NEGATIVE_INFINITY;
    var tmp;
    for (var i=equity.length-1; i>=0; i--) {
        tmp = equity[i].y;
        if (tmp < lowest) lowest = tmp;
        if (tmp > highest) highest = tmp;
    }

    var chart = new CanvasJS.Chart("chartEquity", {
		title:{
			text: "Evolution de la valeur des titres"              
        },
        axisY:{
               minimum: lowest - 10,
               maximum: highest + 10,
               title: "Euros",
              },
        axisX:{
        title: "Date"
        },
		data: [              
		{
			// Change type to "doughnut", "line", "splineArea", etc.
			type: "line",
			dataPoints: equity
		}
		]
	});
	chart.render();

}

function ajaxRequest(type, url, dataType, key, arguments){

    jQuery.ajax({
        type: type,
        url: url,
        dataType: dataType,
        data: {[key]: arguments},
    
        success: function (obj) {
                    if(obj){
                        handleAjaxReturn(obj);
                    }   
                }
    });

}


function handleAjaxReturn(obj){

    if(obj == null){
        console.log("Error");
        return;
    }else{
        
    }

    if(obj["code"] == 200){
        switch(obj["action"]){

            case "updateSymbol" :
                alert("Symbole mis à jour");
                window.location.href = 'http://ihm.tradingbot.business/symbol.php';
                break;
            case "addModel" : 
                console.log("add model");
                break;
            case "addSymbol" :
                alert("Symbole ajouté");
                window.location.href = 'http://ihm.tradingbot.business/symbol.php';
                break;
            case "getNews" : 
                displayNews(obj["message"]);
                break;

        }
    }else{
        console.log("Error code");
        return;
    }

}