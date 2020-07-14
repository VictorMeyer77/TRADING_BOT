<?php 

    include "classes/modelClass.php";
    include "classes/symbolClass.php";
    
    function getAllModelConfig($url){
        
        $url_config = $url."/configuration";
        $contents = file_get_contents($url_config);
        return $contents;
    }

    function getAllSymboles($url){
        
        $url_symbole = $url."/symboles";
        $contents = file_get_contents($url_symbole);
        return $contents;
    }

    function getAllPredictions($url){
        
        $url_account = $url."?collectionName=prediction";
        $contents = file_get_contents($url_account);
        return $contents;
    }

    function getAllNews($url){
        $url_news = $url."/news";
        $contents = file_get_contents($url_news);
        return $contents;
    }

    function getAccountInfo($url){
        $url_account = $url."/accountInfo";
        $contents = file_get_contents($url_account);
        return $contents;
    }

    function getGraphBalanceArray($account){
        
        $balance = array();
        $i =0;

        foreach($account["objects"] as $value){
            $balance[$i]["label"] = date("d/m/yy - h:i:s", $value["dateMaj"]);
            $balance[$i]["y"] = floatval($value["balance"]);
            $i++;
        }

        return $balance;

    }

    function getEquityBalanceArray($account){
        
        $equity = array();
        $i =0;

        foreach($account["objects"] as $value){
            $equity[$i]["label"] = date("d/m/yy - h:i:s", $value["dateMaj"]);
            $equity[$i]["y"] = floatval($value["equity"]);
            $i++;
        }

        return $equity;

    }

    function saveModelConfig($modelParams){


        $model = new Model();
        $model->nbDaysBeforePred = $modelParams[0];
        $model->deltaToTrade = $modelParams[1];
        $model->nbNeurPerLayer = $modelParams[2];
        $model->layerActivation = $modelParams[3];
        $model->nbOutput = $modelParams[4];
        $model->epochs = $modelParams[5];
        $model->batchsize = $modelParams[6];

        $trade = array($modelParams[7],$modelParams[8],$modelParams[9]);
        
        $result = array("code" => 200, "action" => "addModel");

        echo json_encode($result);
    }

    function addSymbol($params){

        $symbol = new Symbol();
        $symbol->_id = $params[0];
        $symbol->nom = $params[1];
        $symbol->mt_id = str_replace("#", "%23", $params[2]);
        $symbol->secteur = $params[3];
        $symbol->supersecteur = $params[4];
        $symbol->pays = $params[5];
        $symbol->actif = $params[6] == "true" ? 1 : 0;

        $symbol = json_encode($symbol);

        $url = "http://tradingbot4iabd.hopto.org/updateSymbole?symbole=".$symbol;

        $curl_handle=curl_init();
        curl_setopt($curl_handle, CURLOPT_URL,$url);
        curl_setopt($curl_handle, CURLOPT_HEADER, 0);
        curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl_handle, CURLOPT_AUTOREFERER, true);
        curl_setopt($curl_handle, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($curl_handle,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17');
        $query = curl_exec($curl_handle);
        
        curl_close($curl_handle);

        if($query == "1"){
            $result = array("code" => 200, "action" => "addSymbol", "message" => $symbol);
        }else{
            $result = array("code" => 400);
        }

        echo json_encode($result);
    }

    function updateSymbol($symbolParams){

        $actif = $symbolParams[1] == "active" ? 1 : 0;

        $json = '{';
        $json .= '"_id":"'.strval($symbolParams[0]).'",'; 
        $json .= '"actif":'.$actif;
        $json .= '}';

        $url = "http://tradingbot4iabd.hopto.org/updateSymbole?symbole=".$json;

        $curl_handle=curl_init();
        curl_setopt($curl_handle, CURLOPT_URL,$url);
        curl_setopt($curl_handle, CURLOPT_HEADER, 0);
        curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl_handle, CURLOPT_AUTOREFERER, true);
        curl_setopt($curl_handle, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($curl_handle,CURLOPT_USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17');
        $query = curl_exec($curl_handle);
        
        curl_close($curl_handle);

        if($query == "1"){
            $result = array("code" => 200, "action" => "updateSymbol");
        }else{
            $result = array("code" => 400);
        }

        echo json_encode($result);
       
    }

    function getNews($company){

        $url = "http://tradingbot4iabd.hopto.org/ihmapi?collectionName=news&filterColumn=entreprise&filter=" . $company;

        $news = file_get_contents($url);
        $news = json_decode($news, $assoc = true);

        $result = array("code" => 200, "action" => "getNews", "message" => $news);
        echo json_encode($result);
    }

    function modelToJson($model, $trade){
        
        //model
        $json = '{"model":{';
        $json .= '"nbDayBeforePred":'. $model->nbDaysBeforePred . ',';
        $json .= '"deltaToTrade":'. $model->deltaToTrade . ',';
        $json .= '"nbNeurPerLayer":'. $model->nbNeurPerLayer . ',';
        $json .= '"layerActivation":'. $model->layerActivation . ',';
        $json .= '"nbOutput":'. $model->nbOutput . ',';
        $json .= '"epochs":'. $model->epochs . ',';
        $json .= '"batchsize":'. $model->batchsize;
        $json .= '},';

        //trade
        $json .= '"trade":{';
        $json .= '"moneyByTrade":'. $trade[0] . ',';
        $json .= '"stoploss":'. $trade[1] . ',';
        $json .= '"takeprofit":'. $trade[2];
        $json .= '}}';


        return $json;
    }
    

    if(isset($_POST['saveModel'])){
        saveModelConfig($_POST['saveModel']);
    }

    if(isset($_POST['udpateSymbol'])){
        updateSymbol($_POST['udpateSymbol']);
    }

    if(isset($_POST['addSymbol'])){
        addSymbol($_POST['addSymbol']);
    }

    if(isset($_POST['getNews'])){
        getNews($_POST['getNews']);
    }

?>