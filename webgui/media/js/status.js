/*             
 Copyright (C) 2013 Daniil Egorov <datsideofthemoon@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var liveStatusURL="/openbts/status/";
var intervalID;

function GetCellID(msg)
{
  var innerHTML;
  //var msg=GetCommand("cellid");
  //if (msg=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Cell ID</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>MCC:</td><td>"+msg[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>MNC:</td><td>"+msg[1]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>LAC:</td><td>"+msg[2]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>CI:</td><td>"+msg[3]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetLoad(msg)
{
  var innerHTML;
  var load_arr=msg;
  //if (load_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Load</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>SDCCH load:</td><td>"+load_arr[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>TCH/F load:</td><td>"+load_arr[1]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>AGCH/PCH load:</td><td>"+load_arr[2]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>Paging table size:</td><td>"+load_arr[3]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>Transactions/TMSIs:</td><td>"+load_arr[4]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>T3122:</td><td>"+load_arr[5]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetPower(msg)
{
  var innerHTML;
  var power_arr=msg;
  //if (power_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";  
  innerHTML+="<h2>Power</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>"+power_arr[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>"+power_arr[1]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetNoise(msg)
{
  var innerHTML;
  var noise_arr=msg;
  //if (noise_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">"; 
  innerHTML+="<h2>Noise</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>"+noise_arr[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>"+noise_arr[1]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetRegPeriod(msg)
{
  var innerHTML;
  var regperiod_arr=msg;//GetCommand("regperiod");
  //if (regperiod_arr=="not connected")
  //{
  // return null;
  //}
  innerHTML="<div class=\"borderdiv\">"; 
  innerHTML+="<h2>Registration period</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>"+regperiod_arr[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>"+regperiod_arr[1]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetUptime(msg)
{
  var innerHTML;
  var uptime_arr=msg;//GetCommand("uptime");
  //if (uptime_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Uptime</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>"+uptime_arr[0]+"</td></tr>";
  innerHTML+="<tr class=\"trheader\"><td>"+uptime_arr[1]+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetVersion(msg)
{
  var innerHTML;
  var vers=msg;//GetCommand("version");
  //if (vers=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Version</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>"+vers+"</td></tr>";
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetChans(msg)
{
  var innerHTML;
  var chans_arr=msg;//GetCommand("chans");
  //if (chans_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Channels</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>CN</td><td>TN</td><td>Chan type</td><td>Transaction Id</td><td>UPFER pct</td><td>RSSI dB</td><td>TXPWR dBm</td><td>TXTA sym</td><td>DNLEV dBm</td><td>DNBER pct</td></tr>";
  for (var key in chans_arr)
  {
    var val = chans_arr[key];
    innerHTML+="<tr><td>"+val[0]+"</td><td>"+val[1]+"</td><td>"+val[2]+"</td><td>"+val[3]+"</td><td>"+val[4]+"</td><td>"+val[5]+"</td><td>"+val[6]+"</td><td>"+val[7]+"</td><td>"+val[8]+"</td><td>"+val[9]+"</td></tr>";
  }
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetTMSIs(msg)
{
  var innerHTML;
  var tmsis_arr=msg;//GetCommand("tmsis");
  //if (tmsis_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>TMSIs</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>TMSI</td><td>IMSI</td><td>Age</td><td>Used</td></tr>";
  for (var key in tmsis_arr)
  {
    var val = tmsis_arr[key];
    innerHTML+="<tr><td>"+val[0]+"</td><td>"+val[1]+"</td><td>"+val[2]+"</td><td>"+val[3]+"</td></tr>";
  }
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}
function GetCalls(msg)
{
  var innerHTML;
  var calls_arr=msg;//GetCommand("calls");
  //if (calls_arr=="not connected")
  //{
  //  return null;
  //}
  innerHTML="<div class=\"borderdiv\">";
  innerHTML+="<h2>Calls</h2>";
  innerHTML+="<table class=\"status\">";
  innerHTML+="<tr class=\"trheader\"><td>Transaction ID</td><td>IMSI</td><td>SIP Call ID</td><td>Caller ID</td><td>GSM State</td><td>SIP State</td><td>Time</td></tr>";
  for (var key in calls_arr)
  {
    var val = calls_arr[key];
    innerHTML+="<tr><td>"+val[0]+"</td><td>"+val[1]+"</td><td>"+val[2]+"</td><td>"+val[3]+"</td><td>"+val[4]+"</td><td>"+val[5]+"</td><td>"+val[6]+"</td></tr>";
  }
  innerHTML+="</table>";
  innerHTML+="</div>";
  return innerHTML;
}


function GetRequest()
{
  var msg=jQuery.parseJSON($.ajax({type:"POST",url: liveStatusURL, async: false}).responseText);
  if (msg=="not connected") return null;
  return msg;
}


function UpdatePage()
{
  var data=GetRequest();
  if (data==null)
  {
    clearInterval(intervalID);
    $('div#content').html("<h2>Error connecting to OpenBTS. Check if its running.</h2>");
  }
  var innerHTML="";
  innerHTML+=GetCellID(data[0]);
  innerHTML+=GetLoad(data[1]);
  innerHTML+=GetPower(data[2]);
  innerHTML+=GetNoise(data[3]);
  innerHTML+=GetRegPeriod(data[4]);
  innerHTML+=GetUptime(data[5]);
  innerHTML+=GetVersion(data[6]);
  innerHTML+=GetChans(data[7]);
  innerHTML+=GetTMSIs(data[8]);
  innerHTML+=GetCalls(data[9]);

  $('div#content').html(innerHTML);

}
function LoadData()
{
  UpdatePage();
  intervalID=setInterval(UpdatePage,500);
}
