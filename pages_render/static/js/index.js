async function callClick(){
  let response = await fetch('http://localhost:8000/click/',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("data").innerHTML = answer;
}

async function getUser(id){
  let response = await fetch('http://localhost:8000/users/' + id,{
    method: 'GET'
  });
  let answer = await response.json();

  document.getElementById("user").innerHTML = answer['username'];
  let getCycle = await fetch('http://localhost:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];


  if(cycle['boosts'].length != 0){
      let getBoost = await fetch('http://localhost:8000/boosts/' + cycle['boosts'][0],{
        method: 'GET'
      });
      let boost = await getBoost.json();
      document.getElementById("boostLevel").innerHTML = boost['level'];
      document.getElementById("boostCost").innerHTML = boost['price'];
  }else{
      document.getElementById("boostLevel").innerHTML = 0;
      document.getElementById("boostCost").innerHTML = 10;
  }
}

async function buyBoost(id, boostId){
  let response = await fetch('http://localhost:8000/buyBoost',{
    method: 'GET'
  });
  let answer = await response.json();
  document.getElementById("clickPower").innerHTML = answer;

  response = await fetch('http://localhost:8000/users/' + id,{
    method: 'GET'
  });
  answer = await response.json();

  let getCycle = await fetch('http://localhost:8000/cycles/' + answer['cycle'],{
    method: 'GET'
  });
  let cycle = await getCycle.json();
  document.getElementById("data").innerHTML = cycle['coinsCount'];

  let getBoost = await fetch('http://localhost:8000/boosts/' + cycle['boosts'][0],{
    method: 'GET'
  });
  let boost = await getBoost.json();
  document.getElementById("boostLevel").innerHTML = boost['level'];
  document.getElementById("boostCost").innerHTML = boost['price'];
}
