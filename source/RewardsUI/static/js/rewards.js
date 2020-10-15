function buildCell(dataPoint){
  var cell = document.createElement('td'),
  textNode = document.createTextNode(dataPoint);
  cell.classList.add('paddingTop10px');
  cell.appendChild(textNode);
  return cell;
}
function resetData(data){
    getClientRewards('');
}
function submitForm(){
  var email = document.getElementById('email').value,
  amount = document.getElementById('amount').value,
  client = new XMLHttpRequest();

  if(email === '' || amount === ''){
      openSnackbar('snackbarRequiredInformation', 10000);
  }else{
      client.onreadystatechange = function() {
        if (client.readyState === 4) {
            document.getElementById('buttonAddRewards').style.display = 'inline-block';
            document.getElementById('divAddRewardsIndicator').style.display = 'none';
            if(client.response === ''){
                openSnackbar('snackbarError', 4000);
            }else{
                openSnackbar('snackbarSuccess', 4000);
                resetData(JSON.parse(client.response));
            }
        }
      }
      document.getElementById('buttonAddRewards').style.display = 'none';
      document.getElementById('divAddRewardsIndicator').style.display = 'inline-block';
      client.open("POST", "http://localhost:7050/orders", true);
      client.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      client.send("email=" + email + "&amount=" + amount);
  }
}
function displayData(data) {
  var tblClientRewards = document.getElementById('tblClientRewards'),
  tblBody = document.createElement('tbody');
  tblClientRewards.removeChild(tblClientRewards.getElementsByTagName('tbody')[0]);
  tblClientRewards.appendChild(tblBody);
  for(var i=0;i<data.length;i++){
    var entry = data[i];
    var row = document.createElement('tr');
    row.appendChild(buildCell(entry.email));
    row.appendChild(buildCell(entry.points));
    row.appendChild(buildCell(entry.tier));
    row.appendChild(buildCell(entry.tierName));

    row.appendChild(buildCell(entry.nextTier === '' ? '-' : entry.nextTier));
    row.appendChild(buildCell(entry.nextTierName === '' ? '-' : entry.nextTierName));
    row.appendChild(buildCell(entry.nextTierProgress === 0 ? '-' : entry.nextTierProgress));
    tblBody.appendChild(row);
  }
  tblClientRewards.appendChild(tblBody);
  document.getElementById('tblClientRewards').style.display = 'table';
  document.getElementById('divClientRewardsIndicator').style.display = 'none';

}
function getClientRewards(email){
  var client = new XMLHttpRequest(),
  data = null,
  param = (email === '') ? '' : '?email=' + email;

  document.getElementById('tblClientRewards').style.display = 'none';
  document.getElementById('divClientRewardsIndicator').style.display = 'block';

  client.onreadystatechange = function() {
    if (client.readyState === 4) {
      displayData(JSON.parse(client.response));
    }
  }

  client.open('GET', 'http://localhost:7050/orders' + param, true);
  client.send();
}
function adjustAddPanel(){
    var divAddPanel = document.getElementById('divAddPanel'),
    divAddButton = document.getElementById('divAddButton');
    divAddButton.classList.toggle("active");
    if (divAddPanel.style.maxHeight) {
        divAddPanel.style.maxHeight = null;
    } else {
        divAddPanel.style.maxHeight = divAddPanel.scrollHeight + "px";
    }
}
function openSnackbar(snackbarId, timeDelay){
  var x = document.getElementById(snackbarId);
  x.className = "show";
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, timeDelay);
}
