function buildCell(dataPoint){
  var cell = document.createElement('td'),
  textNode = document.createTextNode(dataPoint);
  cell.appendChild(textNode);
  return cell;
}
function submitForm(){
  var email = document.getElementById('email').value,
  amount = document.getElementById('amount').value,
  client = new XMLHttpRequest();

  client.open("POST", "http://localhost:7050/orders", true);
  client.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  client.send("email=" + email + "&amount=" + amount);
}
function displayData(data) {
  var tblClientRewards = document.getElementById('tblClientRewards'),
  tblBody = document.createElement('tbody');
  tblClientRewards.removeChild(tblClientRewards.getElementsByTagName('tbody')[0]);
  //tblClientRewards.removeChild(tblClientRewards.getElementsByTagName('tbody'));
  tblClientRewards.appendChild(tblBody);
  for(var i=0;i<data.length;i++){
    var entry = data[i];
    var row = document.createElement('tr');
    row.appendChild(buildCell(entry.email));
    row.appendChild(buildCell(entry.points));
    row.appendChild(buildCell(entry.tier));
    row.appendChild(buildCell(entry.tierName));
    row.appendChild(buildCell(entry.nextTier));
    row.appendChild(buildCell(entry.nextTierName));
    row.appendChild(buildCell(entry.nextTierProgress));
    tblBody.appendChild(row);
  }
  tblClientRewards.appendChild(tblBody);

}
function getClientRewards(email){
  var client = new XMLHttpRequest(),
  data = null,
  param = (email === '') ? '' : '?email=' + email;

  client.onreadystatechange = function() {
    if (client.readyState === 4) {
      displayData(JSON.parse(client.response));
    }
  }

  client.open('GET', 'http://localhost:7050/orders' + param, true);
  client.send();
}
/* BEG: OnLoad function calls */
getClientRewards('');
/* END: OnLoad function calls */
