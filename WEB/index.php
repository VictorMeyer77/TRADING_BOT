<?php 

  include "methods.php";
  include "vars.php";

  $symboles = getAllSymboles($url_api);
  $symboles = json_decode($symboles, $assoc = true);

  $predictions = getAllPredictions($url_api);
  $predictions = json_decode($predictions, $assoc = true);

  usort($predictions["objects"], function($a, $b) {
    return intval($a['datePred']) - intval($b['datePred']);
  });

  $account = getAccountInfo($url_api); 
  $account = json_decode($account, $assoc = true);

  usort($account["objects"], function($a, $b) {
    return intval($a['dateMaj']) - intval($b['dateMaj']);
  });

  $balance = getGraphBalanceArray($account);
  $equity = getEquityBalanceArray($account);

  arsort($predictions["objects"]);
  arsort($account["objects"]);

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
  <body onload='buildGraphBalance(<?php echo json_encode($balance); ?>); buildGraphEquity(<?php echo json_encode($equity); ?>)'>
  <?php include "menu.php"; ?> 

  <div class="custom-separator">
      <h2 class="text-center">Actualités</h2>
    </div>

  <div class="container">
      <form style = "width : 18rem;">
        <div class="form-group">
          <label for="exampleFormControlSelect1">Sélectionner une entreprise</label>
          <select id="selectCompany" onchange="getNews()" class="form-control align-center" id="companyNews">
            <?php foreach($symboles["objects"] as $value){
              if(isset($value["nom"])) echo '<option>'.$value["nom"].'</option>';
            }?>
          </select>
        </div>
      </form>

      <div class="row" id = "divNews"></div>
      
  </div>
  <br><br>
  <div class="custom-separator">
      <h2 class="text-center">Dernières prédictions</h2>
  </div>

  <div class="container">
      <div class="row" id = "divPredictions">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>symbole</th>
              <th>Action</th>
              <th>Jours d'écart</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <?php 
            $counter = 0;
            foreach($predictions["objects"] as $value){  
              
              switch($value["trend"]){
                case 0 :
                  $trend = "Standby";
                break;

                case 1 :
                  $trend = "Achat";
                break;

                case 0 :
                  $trend = "Vente";
                break;
                

              }

              ?>

              <tr>
                <td><?php echo $value["symbole"]; ?></td>
                <td><?php echo $trend; ?></td>
                <td><?php echo $value["period"]; ?></td>
                <td><?php echo date("d/m/yy h:i:s", $value["datePred"]); ?></td>
            <?php 
            $counter ++;
            if($counter >= 9) break;  
          }?>
              </tr>
          </tbody>
        </table>
    </div> 
  </div>

  <div class="custom-separator">
      <h2 class="text-center">Trading</h2>
  </div>
  <br><br>
  <div class = "container">
          <div class = row>
            <div id="chartBalance" style="padding: 10px;height: 300px; width: 100%;"></div>
            <br><br><br><br>
            <div id="chartEquity" style="padding: 10px;height: 300px; width: 100%;"></div>
          </div>
  </div>
  <br><br><br>
 
    <?php include "footer.php"; ?>
    <?php include "scripts.php";?>
  </body>
</html>