//+------------------------------------------------------------------------------------------+
//|                                                                            TradeInfo.mqh |
//|                         Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer |
//|                                             https://github.com/VictorMeyer77/TRADING_BOT |
//+------------------------------------------------------------------------------------------+
#property copyright "Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer"
#property link      "https://github.com/VictorMeyer77/TRADING_BOT"

#include <Trade\PositionInfo.mqh>

int SendTradeInfo(ulong ticket, string status){
   
   CPositionInfo pos;
   char post[];
   char result[];
   string headers;
   string url = "http://tradingbot4iabd.hopto.org/insertTradeInfo?";
   string symbole = pos.Symbol();
   StringReplace(symbole, "#", "!");
   
   if(pos.SelectByTicket(ticket)){
      
      url += "symbole=";
      url += symbole;
      url += "&type=";
      url += (string)pos.PositionType();
      url += "&status=";
      url += status;
      url += "&swap=";
      url += (string)pos.Swap();
      url += "&comission=";
      url += (string)pos.Commission();
      url += "&priceCurrent=";
      url += (string)pos.PriceCurrent();
      url += "&priceOpen=";
      url += (string)pos.PriceOpen();
      url += "&profit=";
      url += (string)pos.Profit();
      url += "&stoploss=";
      url += (string)pos.StopLoss();
      url += "&takeprofit=";
      url += (string)pos.TakeProfit();
      url += "&dateMaj=";
      url += (string)((ulong)TimeCurrent() - 4 * 60 * 60);
      
   }
  
   int res = WebRequest("GET", url, NULL, NULL, 500, post, 0, result, headers);
   
   if(res == 200)
      return 1;
   return -1;
}

void LaunchTradeInfos(){
   
   for(int i = 0; i < PositionsTotal(); i += 1){
      int res = SendTradeInfo(PositionGetTicket(i), "RUNNING");
      if(res == -1){
         Print("Failed to insert trade info " + (string)PositionGetTicket(i));
      }
   }
   
}