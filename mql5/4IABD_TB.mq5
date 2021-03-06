//+------------------------------------------------------------------------------------------+
//|                                                                            CsvReader.mqh |
//|                         Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer |
//|                                             https://github.com/VictorMeyer77/TRADING_BOT |
//+------------------------------------------------------------------------------------------+
#property copyright "Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer"
#property link      "https://github.com/VictorMeyer77/TRADING_BOT"
#property version   "1.00"


#include <Trade\Trade.mqh>
#include <NewsLib\Predictions.mqh>
#include <NewsLib\AccountInfo.mqh>
#include <NewsLib\TradeInfo.mqh>
#include <NewsLib\TradeParameter.mqh>


double stoploss;
double takeprofit;
int moneyByTrade;
ulong lastPredTime = 0;
ulong tradeParameterFlag¨= 0;
ulong accountInfoFlag = 0;
ulong tradeInfoFlag = 0;


void OnInit(){

   int res = SetTradeParameter();
   if(res == -1) ExpertRemove();
   
}




void OnTick(){
   

   if((ulong)TimeCurrent() > lastPredTime + (60 * 60) && IsEuronextOpen()){
      if(lastPredTime == 0){
         ManagePredictions((ulong)TimeCurrent()  - 4 * 60 * 60);
      }
      else{
         ManagePredictions(lastPredTime - (60 * 60));
      }
      lastPredTime = (ulong)TimeCurrent() ;
   }
   
   if((ulong)TimeCurrent() > accountInfoFlag + (60 * 60 * 2)){
      SendAccountInfo();
      accountInfoFlag = (ulong)TimeCurrent() ;
   }
   
   if((ulong)TimeCurrent() > tradeParameterFlag¨+ (60 * 60 * 4))
      SetTradeParameter();
   
   if((ulong)TimeCurrent() > tradeInfoFlag + (60 * 60 * 2)){
      LaunchTradeInfos();
      tradeInfoFlag = (ulong)TimeCurrent() ;
   }
   
   
}


// ---- met à jour les paramètres de trading ---- //

int SetTradeParameter(){

   tradeParameter tradeParam = GetTradeParameter();
   stoploss = tradeParam.stoploss;
   takeprofit = tradeParam.takeprofit;
   moneyByTrade = tradeParam.moneyByTrade;
   tradeParameterFlag¨= (ulong)TimeCurrent() ;
   
   if(stoploss < 0 && takeprofit < 0 && moneyByTrade < 0){
      Print("Impossible de récupérer les paramètres de trading");
      return -1;
   }
   else{
      Print("Stoploss: " + DoubleToString(stoploss) +
       " / Takeprofit: " + DoubleToString(takeprofit) +
        " / moneyByTrade: " + DoubleToString(moneyByTrade));
      return 1;
   }
   
}

// ---- récupère et traite les prédictions ---- //

void ManagePredictions(ulong flag){

   prediction predictions[];
   GetPredictions(predictions, flag);
   for(int i = 0; i < ArraySize(predictions); i += 1){
      
      Print("Symbole: " + predictions[i].symbole +
       " --> Prédiction " + (string)predictions[i].pred);
      
      ulong ticket = GetTicketBySymbole(predictions[i].symbole);
      if(ticket == 0){
      
         int volume = 0;
         if(predictions[i].pred == 1) volume = GetVolumePerTrade(predictions[i].symbole, 0);
         if(predictions[i].pred == 2) volume = GetVolumePerTrade(predictions[i].symbole, 1);
         
         if(volume == 0) continue;
         
         OpenPosition(predictions[i].symbole, predictions[i].pred - 1,
                        volume, predictions[i].nbDayValid);
         
      }
      else{
         
         int posistionType = GetPositionTypeByTicket(ticket);
         
         if(predictions[i].pred == 0) continue;
         
         if(predictions[i].pred - 1 != GetPositionTypeByTicket(ticket)){
            CTrade trade;
            trade.PositionClose(ticket);
         }
         
      }
      
   }
   

}

// ---- récupère le ticket d'un trade à partir d'un symbole ---- //

ulong GetTicketBySymbole(string symbole){
   
   ulong ticket = 0;
   for(int i = 0; i < PositionsTotal(); i += 1){
      if(PositionGetSymbol(i) == symbole) ticket = PositionGetTicket(i);
   }
   
   return ticket;
}

// ---- retourne le type d'ordre d'un ticket ---- //

int GetPositionTypeByTicket(ulong ticket){
   CPositionInfo pos;
   if(pos.SelectByTicket(ticket)){
      return pos.PositionType();
   }
   return -1;
}

// ---- calcul le volume à acheter ---- //

int GetVolumePerTrade(string symbole, int positionType){
   if(SymbolInfoDouble(symbole, SYMBOL_ASK) < 0.001){
      Print("Symbole non reconnu: " + symbole);
      return 0;
   }
   if(positionType == 0) return (int)(moneyByTrade / SymbolInfoDouble(symbole, SYMBOL_ASK));
   if(positionType == 1) return (int)(moneyByTrade / SymbolInfoDouble(symbole, SYMBOL_BID));
   return 0;
}

// ---- ouvre une position ---- //

void OpenPosition(string symbole, int positionType, int volume, int nbDayValid){
   
   CTrade trade;
   if(positionType == 0){
      if(trade.PositionOpen(symbole,
       ORDER_TYPE_BUY,
        volume,
         SymbolInfoDouble(symbole, SYMBOL_ASK),
          SymbolInfoDouble(symbole, SYMBOL_ASK) * (1 - stoploss / 100),
           SymbolInfoDouble(symbole, SYMBOL_ASK) * (1 + takeprofit / 100),
           (string)nbDayValid)){
             Print((string) volume + " " + symbole + " SELL");
      }
    
   }
   else{
      if(trade.PositionOpen(symbole,
       ORDER_TYPE_SELL,
        volume,
         SymbolInfoDouble(symbole, SYMBOL_BID),
          SymbolInfoDouble(symbole, SYMBOL_BID) * (1 - stoploss / 100),
           SymbolInfoDouble(symbole, SYMBOL_BID) * (1 + takeprofit / 100),
           (string)nbDayValid)){
            Print((string) volume + " " + symbole + " SELL");
      }
      
   }
   
   
}

// ---- ferme les positions dont la prédiction est trop ancienne ---- //

void CloseOldPos(){
   
   CPositionInfo pos;
   for(int i = 0; i < PositionsTotal(); i += 1){
   
      if(pos.SelectByIndex(i)){
      
         ulong dateOpen;
         pos.InfoInteger(POSITION_TIME, dateOpen);
         int nbDayValid = (int)pos.Comment();
         
         if(dateOpen + nbDayValid * (60 * 60 * 24) > (ulong)TimeCurrent() ){
            CTrade trade;
            
            if(pos.Profit() > 0){
             trade.PositionModify(pos.Ticket(), pos.PriceOpen(), pos.TakeProfit());
            }
            else{
              trade.PositionClose(pos.Ticket());
              SendTradeInfo(pos.Ticket(), "CLOSE");
            }
              
         }
      }
   }
   
}

// ---- retourne true si les marchés sont ouverts ---- //

bool IsEuronextOpen(){

   ENUM_DAY_OF_WEEK week[] = {SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY};
   MqlDateTime now;
   MqlDateTime from;
   MqlDateTime to;
   datetime fromdt;
   datetime todt;
   
   TimeToStruct(TimeCurrent(), now);
   SymbolInfoSessionQuote("#RMS", week[now.day_of_week], 0, fromdt, todt);

   TimeToStruct(fromdt, from);
   TimeToStruct(todt, to);
   if(now.hour > from.hour && now.hour < to.hour){
      return true;
   }
   else{
      return false;
   }

}