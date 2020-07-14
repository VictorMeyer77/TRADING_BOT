<?php
    error_reporting(E_ALL);
    ini_set('display_errors', TRUE);
    ini_set('display_startup_errors', TRUE);

    include "methods.php";
    include "vars.php";

    $symboles = getAllSymboles($url_api);
    $symboles = json_decode($symboles, $assoc = true);

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
      <h2 class="text-center">Gestion des symboles</h2><br>

      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#addSymbol" aria-expanded="false" aria-controls="addSymbol">
        Ajouter un symbole
      </button>
      <br><br>
      <div class="row collapse" id="addSymbol">
        <div class="card center-block" style="width: 45rem;margin :auto;" id = "formSymbol">  
          <form>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">Id symbole</label>
                <input name="paramSymbol" type="text" class="form-control" id="formId" placeholder="3">
            </div>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">Nom</label>
                <input name="paramSymbol" type="text" class="form-control" id="formName" placeholder="3">
            </div>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">Mt id</label>
                <input name="paramSymbol" type="text" class="form-control" id="formMtId" placeholder="3">
            </div>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">secteur</label>
                <input name="paramSymbol" type="text" class="form-control" id="formSecteur" placeholder="3">
            </div>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">supersecteur</label>
                <input name="paramSymbol" type="text" class="form-control" id="formSuperSecteur" placeholder="3">
            </div>
            <div class="form-group" style="margin: auto; width: 20rem;">
                <label for="formGroupExampleInput">Pays</label>
                <input name="paramSymbol" type="text" class="form-control" id="formPays" placeholder="3">
            </div>
            <div class="form-check" style="margin: auto; width: 20rem;">
              <label class="form-check-label" for="exampleCheck1">Active</label>
              <input style = "left:20px;" name="paramSymbol" type="checkbox" class="form-check-input" id="formActive">
            </div>
          </form>
          <br>
          <button onclick = "addSymbol()" class="btn btn-success  text-center" style="width: 10rem;margin :auto;" type="button">
              Ajouter
          </button>
          <button class="btn btn-danger  text-center" style="width: 10rem;margin :auto;" type="button" data-toggle="collapse" data-target="#addSymbol" aria-expanded="false" aria-controls="addSymbol">
              Annuler
          </button>
          <br>
        </div>
        <br><br>
      </div>

        <table class="table table-hover">
          <thead>
            <tr>
              <th>Id symbole</th>
              <th>Nom</th>
              <th>Mt id</th>
              <th>secteur</th>
              <th>supersecteur</th>
              <th>Pays</th>
              <th>Actif</th>
              <th>Modifier</th>
            </tr>
          </thead>
          <tbody>
            <?php foreach($symboles["objects"] as $value){ ?>
            <tr>
              <td><?php echo $value["_id"]?></td>
              <td><?php echo $value["nom"]?></td>
              <td><?php echo $value["mt_id"]?></td>
              <td><?php echo $value["secteur"] ?></td>
              <td><?php echo $value["supersecteur"]?></td>
              <td><?php echo $value["pays"] ?></td>
              <td><?php echo $string = ($value["actif"] == 1) ? "Oui" : "Non" ?></td>
              <td>
                <button onclick='<?php echo $string = $value["actif"] == 1 ? "actionSymbol(".json_encode($value["_id"]).", `deactive`)" : "actionSymbol(".json_encode($value["_id"]).", `active`)";?>' class='<?php echo $string = $value["actif"] == 1 ? "btn btn-danger" : "btn btn-primary";?>' type="button">
                    <?php echo $string = $value["actif"] == 1 ? "Désactiver" : "Activer";?>
                </button>
              </td>
            </tr>
            <?php }?>
          </tbody>
      </table>
  
      <?php include "footer.php"?>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <?php include "scripts.php";?> 
  </body>
</html>