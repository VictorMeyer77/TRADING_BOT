//+------------------------------------------------------------------------------------------+
//|                                                                          AccountInfo.mqh |
//|                         Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer |
//|                                             https://github.com/VictorMeyer77/TRADING_BOT |
//+------------------------------------------------------------------------------------------+
#property copyright "Copyright 2020, Baptiste Fauvert, Alexandre Mathieu Victor Meyer"
#property link      "https://github.com/VictorMeyer77/TRADING_BOT"


int SendAccountInfo(){
   
   char post[];
   char result[];
   string headers;
   string url = "http://tradingbot4iabd.hopto.org/insertAccountInfo?";
   
   url += "currency=";
   url += AccountInfoString(ACCOUNT_CURRENCY);
   url += "&name=";
   url += AccountInfoString(ACCOUNT_NAME);
   url += "&tradeMode=";
   url += (string)AccountInfoInteger(ACCOUNT_TRADE_MODE);
   url += "&login=";
   url += (string)AccountInfoInteger(ACCOUNT_LOGIN);
   url += "&company=";
   url += AccountInfoString(ACCOUNT_COMPANY);
   url += "&leverage=";
   url += (string)AccountInfoInteger(ACCOUNT_LEVERAGE);
   url += "&balance=";
   url += (string)AccountInfoDouble(ACCOUNT_BALANCE);
   url += "&equity=";
   url += (string)AccountInfoDouble(ACCOUNT_EQUITY);
   url += "&profit=";
   url += (string)AccountInfoDouble(ACCOUNT_PROFIT);
   url += "&dateMaj=";
   url += (string)((ulong)TimeCurrent() - 4 * 60 * 60);

   int res = WebRequest("GET", url, NULL, NULL, 500, post, 0, result, headers);
   
   if(res == 200)
      return 1;
   return -1;
   
}