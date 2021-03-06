//+------------------------------------------------------------------------------------------+
//|                                                                       TradeParameter.mqh |
//|                         Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer |
//|                                             https://github.com/VictorMeyer77/TRADING_BOT |
//+------------------------------------------------------------------------------------------+
#property copyright "Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer"
#property link      "https://github.com/VictorMeyer77/TRADING_BOT"



struct tradeParameter{
   double stoploss;
   double takeprofit;
   int moneyByTrade;
};

// ---- retourne un tableau de valeur à partir d'une ligne de prédiction ---- //

void GetTradeParameterCols(string& cols[], string row){
   int res = StringSplit(row, StringGetCharacter(",", 0), cols);
}

// ---- recupere le parametrage du trading ---- //

string GetTradeParameterCsv(){
   
   char post[];
   char result[];
   string headers;
   string url = "http://tradingbot4iabd.hopto.org/getTradeParameter";
   int res = WebRequest("GET", url, NULL, NULL, 500, post, 0, result, headers);
   string csvString = CharArrayToString(result);
  
   if(res == 200 && csvString != "ERROR")
      return csvString;
   return "ERROR";
   
}

// ---- retourne le paramétrage du trading ---- //

tradeParameter GetTradeParameter(){

   string cols[];
   GetTradeParameterCols(cols, GetTradeParameterCsv());
   tradeParameter tp;
   if(ArraySize(cols) == 3){
      tp.stoploss = (double)cols[0];
      tp.takeprofit = (double)cols[1];
      tp.moneyByTrade = (int)cols[2];
   }
   else{
      tp.stoploss = -1.0;
      tp.takeprofit = -1.0;
      tp.moneyByTrade = -1;      
   }
   
   return tp;
}

