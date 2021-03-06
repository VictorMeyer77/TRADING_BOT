//+------------------------------------------------------------------------------------------+
//|                                                                          Predictions.mqh |
//|                         Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer |
//|                                             https://github.com/VictorMeyer77/TRADING_BOT |
//+------------------------------------------------------------------------------------------+
#property copyright "Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer"
#property link      "https://github.com/VictorMeyer77/TRADING_BOT"


// ---- Structure représentant une prédiction ---- //

struct prediction{
   string symbole;
   int pred;
   int nbDayValid;
   ulong datepred;
};


// ---- requete la base mongodb pour récupérer les predictions format csv ---- //

string GetPredictionsCsv(ulong flag){
   
   char post[];
   char result[];
   string headers;
   string url = "http://tradingbot4iabd.hopto.org/oracle/" + (string)(flag);
   int res = WebRequest("GET", url, NULL, NULL, 500, post, 0, result, headers);
   string csvString = CharArrayToString(result);
   
   if(res == 200 && csvString != "ERROR")
      return csvString;
   return "ERROR";
   
}

// ---- retourne un tableau des prédictions à partir du csv ---- //

void GetPredictionsRows(string& rows[], string csv){
   int res = StringSplit(csv, StringGetCharacter(";", 0), rows);
   ArrayRemove(rows, ArraySize(rows) - 1, 1);
}

// ---- retourne un tableau de valeur à partir d'une ligne de prédiction ---- //

void GetPredictionsCols(string& cols[], string row){
   int res = StringSplit(row, StringGetCharacter(",", 0), cols);
}

// ---- créer un structure prédiction ---- //

prediction createPrediction(string row){
   string cols[];
   GetPredictionsCols(cols, row);
   prediction pred;
   pred.symbole = cols[0];
   pred.pred = (int)cols[1];
   pred.nbDayValid = (int)cols[2];
   pred.datepred = (ulong)cols[3];
   return pred;
}

// hydrate un tableau avec les prédictions à traiter ---- //

void GetPredictions(prediction& predictions[], ulong flag){
   
   string csv = GetPredictionsCsv(flag - (4 * 60 * 60));
   if(csv != "ERROR" || csv != ""){

      string rows[];
      GetPredictionsRows(rows, csv);
      ArrayResize(predictions, ArraySize(rows));
      for(int i = 0; i < ArraySize(rows); i += 1){
         predictions[i] = createPrediction(rows[i]);

      }
      
   }

}



