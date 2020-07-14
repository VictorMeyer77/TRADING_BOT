<?php
    error_reporting(E_ALL);
    ini_set('display_errors', TRUE);
    ini_set('display_startup_errors', TRUE);

    include "methods.php";
    include "vars.php";

    $content = getAllModelConfig($url_api);
    $content = json_decode($content, $assoc = true);

?>

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <?php include "links.php";?>
    
    <title>Trading bot</title>
  </head>
  <body>
  <?php include "menu.php" ?> 
    <br>
  <div class="container">
    <h2 class="text-center">Modèles entraînés</h2><br>
    <table class="table table-hover">
      <thead>
        <tr>
          <th>Id model</th>
          <th>Jours avant la prédiction</th>
          <th>Delta de trade(%)</th>
          <th>Format</th>
          <th>Activations</th>
          <th>Nombre de sorties</th>
          <th>Epochs</th>
          <th>Batchsize</th>
          <th>Argent investi par trade</th>
          <th>Stop loss</th>
          <th>Take profit</th>

        </tr>
      </thead>
      <tbody>
        <?php foreach($content["objects"] as $value){ ?>
        <tr>
          <td style = "width:100%;"><?php echo $value["_id"]["\$oid"] ?></td>
          <td><?php echo $value["model"]["nbDayBeforePred"] ?></td>
          <td><?php echo $value["model"]["deltaToTrade"] ?></td>
          <td><?php echo json_encode($value["model"]["nbNeurPerLayer"]) ?></td>
          <td><?php echo json_encode($value["model"]["layerActivation"]) ?></td>
          <td><?php echo $value["model"]["nbOutput"] ?></td>
          <td><?php echo $value["model"]["epochs"] ?></td>
          <td><?php echo $value["model"]["batchSize"] ?></td>
          <td><?php echo $value["trade"]["moneyByTrade"] ?></td>
          <td><?php echo $value["trade"]["stoploss"] ?></td>
          <td><?php echo $value["trade"]["takeprofit"] ?></td>
        </tr>
        
      <?php }?>
      </tbody>
    </table>
    <br>
    <div class="row" style ="margin:auto;" >
      <div class="card" style="width: 45rem;margin :auto;">
        <div class="card-body" >
          <h5 class="card-title">Créer une nouvelle configuration de modèle</h5>
          <h6 class="card-subtitle mb-2 text-muted">Veuillez renseigner les champs ci-dessous</h6><br>
          <form>
            <div class="form-group">
                <label for="formGroupExampleInput">Modèle de machine learning</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="3">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Pourcentage d'évolution à partir duquel on effectue une action</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="3">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Structure du modèle</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="[10, 20]">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Fonctions d'activation</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="[“tanh”, “relu”, “softmax”]">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Nombre de classes (output)</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="[“tanh”, “relu”, “softmax”]">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Nombre d'epochs</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="3">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Batchsize</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="1">
            </div>
            <h6 class="card-subtitle mb-2 text-muted">Options de trading</h6><br>
            <div class="form-group">
                <label for="formGroupExampleInput">Argent investi par transaction</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="1">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Stop Loss</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="1">
            </div>
            <div class="form-group">
                <label for="formGroupExampleInput">Take Profit</label>
                <input name="paramModel" type="text" class="form-control" id="formGroupExampleInput" placeholder="1">
            </div>
          
          </form>
          <button onclick="saveModel()" class="btn btn-primary center">Enregistrer</button>
          
        </div>
      </div>
  </div>
    </div>
</div>

 
    <?php include "footer.php"?>
    

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <?php include "scripts.php";?> 
    </body>
</html>